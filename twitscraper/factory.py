"""
twitscraper.factory - Cookie-based client factory.

All patches are applied automatically:
- curl_cffi transport (fixes ConnectTimeout on x.com)
- Real transaction ID generation via x_client_transaction
- user_id extracted from twid cookie

Usage:
    from twitscraper import create_client

    # From a dict
    client = await create_client({"auth_token": "...", "ct0": "..."})

    # From a JSON file
    client = await create_client_from_file("cookies.json")

    # From a raw browser cookie string (Network tab → Cookie header)
    client = await create_client_from_string("auth_token=abc; ct0=xyz; twid=u%3D123")

    # From a browser extension export (EditThisCookie / Cookie-Editor JSON array)
    client = await create_client_from_browser_export('[{"name":"auth_token","value":"..."}]')
"""

import json
import logging
import types
from urllib.parse import unquote

from .client.client import Client

logger = logging.getLogger(__name__)

_DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)


# ---------------------------------------------------------------------------
# HTTP transport
# ---------------------------------------------------------------------------

class _CurlResponse:
    """Wraps curl_cffi response to match the httpx interface twikit expects."""

    def __init__(self, resp):
        self._resp = resp
        self.status_code = resp.status_code
        self.headers = dict(resp.headers)
        self.text = resp.text
        self.content = resp.content
        self.next_request = None

    def json(self):
        return self._resp.json()


class _CurlCffiHttpWrapper:
    """
    Drop-in replacement for httpx.AsyncClient using curl_cffi.AsyncSession.
    Implements the interface twikit needs: request(), cookies.
    """

    def __init__(self, cookies: dict):
        from curl_cffi.requests import AsyncSession
        self._session = AsyncSession(impersonate='chrome120')
        self._cookies_dict = dict(cookies)
        # twikit reads/writes self.http.cookies as a dict
        self.cookies = self._cookies_dict
        for name, value in self._cookies_dict.items():
            self._session.cookies.set(name, value, domain='.x.com')

    async def request(self, method: str, url: str, headers=None, **kwargs):
        # Keep session cookies in sync before each request
        for name, value in self._cookies_dict.items():
            self._session.cookies.set(name, value, domain='.x.com')

        merged = dict(headers) if headers else {}

        if 'timeout' not in kwargs:
            kwargs['timeout'] = 30

        # curl_cffi uses multipart= instead of files=
        if 'files' in kwargs:
            files = kwargs.pop('files')
            from curl_cffi import CurlMime
            mp = CurlMime()
            for field_name, file_tuple in files.items():
                if isinstance(file_tuple, tuple):
                    filename, fileobj, content_type = file_tuple
                    data = fileobj.read() if hasattr(fileobj, 'read') else fileobj
                    mp.addpart(name=field_name, data=data,
                               filename=filename, content_type=content_type)
                else:
                    mp.addpart(name=field_name, data=file_tuple)
            kwargs['multipart'] = mp

        resp = await self._session.request(method, url, headers=merged, **kwargs)

        # Sync new cookies back to dict so twikit can read them
        for k, v in self._session.cookies.items():
            self._cookies_dict[k] = v

        return _CurlResponse(resp)

    async def get(self, url: str, **kwargs):
        return await self.request('GET', url, **kwargs)

    async def post(self, url: str, **kwargs):
        return await self.request('POST', url, **kwargs)

    async def aclose(self):
        await self._session.close()

    def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.aclose()


# ---------------------------------------------------------------------------
# Transaction ID provider
# ---------------------------------------------------------------------------

def _build_transaction_provider(cookies: dict):
    """
    Build a real transaction ID provider using x_client_transaction.
    Returns None if the package is unavailable or initialization fails.
    """
    try:
        from curl_cffi.requests import Session as CurlSession
        from x_client_transaction import ClientTransaction
        from x_client_transaction.utils import get_ondemand_file_url, handle_x_migration
        from bs4 import BeautifulSoup

        session = CurlSession(impersonate='chrome120')
        for name, value in cookies.items():
            session.cookies.set(name, value, domain='.x.com')
        session.headers.update({
            'Referer': 'https://x.com/',
            'X-Twitter-Active-User': 'yes',
        })

        home_page = handle_x_migration(session=session)
        ondemand_url = get_ondemand_file_url(response=home_page)
        if not ondemand_url:
            session.close()
            return None

        od_resp = session.get(ondemand_url, timeout=20)
        od_html = BeautifulSoup(str(od_resp.text or ''), 'html.parser')
        ct = ClientTransaction(home_page_response=home_page, ondemand_file_response=od_html)
        session.close()
        logger.info("Transaction ID provider initialized")
        return ct
    except Exception as e:
        logger.warning(f"Transaction ID provider failed: {e}")
        return None


# ---------------------------------------------------------------------------
# Patching
# ---------------------------------------------------------------------------

def _patch_client(client: Client, cookies: dict) -> None:
    """Apply all patches to a freshly created Client instance."""
    # 1. Replace httpx with curl_cffi
    client.http = _CurlCffiHttpWrapper(cookies)

    # 2. Transaction ID
    ct_provider = _build_transaction_provider(cookies)
    twikit_ct = client.client_transaction
    twikit_ct.home_page_response = True  # bypass the init guard

    async def _noop_init(self, session, headers):
        pass

    twikit_ct.init = types.MethodType(lambda self, s, h: _noop_init(self, s, h), twikit_ct)

    if ct_provider is not None:
        def _generate_tid(self, method, path, **kw):
            try:
                return ct_provider.generate_transaction_id(method=method, path=path)
            except Exception:
                return ""
        twikit_ct.generate_transaction_id = types.MethodType(_generate_tid, twikit_ct)
    else:
        twikit_ct.generate_transaction_id = types.MethodType(
            lambda self, method, path, **kw: "", twikit_ct
        )

    # 3. Set user_id from twid cookie
    twid = cookies.get('twid', '')
    decoded = unquote(twid)
    if decoded.startswith('u='):
        client._user_id = decoded[2:]


# ---------------------------------------------------------------------------
# Cookie parsers
# ---------------------------------------------------------------------------

def _parse_cookie_string(raw: str) -> dict:
    """Parse a raw ``key=value; key=value`` cookie string into a dict."""
    cookies = {}
    for part in raw.split(';'):
        part = part.strip()
        if '=' in part:
            key, _, value = part.partition('=')
            cookies[key.strip()] = value.strip()
    return cookies


def _parse_browser_export(data: list) -> dict:
    """
    Parse a browser cookie export (EditThisCookie / Cookie-Editor JSON format).
    Only cookies for x.com / .x.com are kept.
    """
    cookies = {}
    for item in data:
        domain = item.get('domain', '')
        if 'x.com' not in domain:
            continue
        name = item.get('name', '').strip()
        value = item.get('value', '').strip()
        if name:
            cookies[name] = value
    return cookies


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def create_client(
    cookies: dict,
    language: str = 'en-US',
    user_agent: str = _DEFAULT_USER_AGENT,
) -> Client:
    """
    Create a ready-to-use twikit Client from a cookies dict.

    Parameters
    ----------
    cookies : dict
        Must contain at least ``auth_token`` and ``ct0``.
        ``twid`` is recommended so ``user_id`` is available immediately.
    language : str, default='en-US'
    user_agent : str, optional

    Returns
    -------
    Client

    Example
    -------
    >>> client = await create_client({"auth_token": "...", "ct0": "...", "twid": "u%3D123"})
    >>> me = await client.user()
    """
    if not cookies.get('auth_token') or not cookies.get('ct0'):
        raise ValueError("cookies must contain at least 'auth_token' and 'ct0'")

    client = Client(language=language, user_agent=user_agent)
    _patch_client(client, cookies)
    return client


async def create_client_from_file(
    path: str,
    language: str = 'en-US',
    user_agent: str = _DEFAULT_USER_AGENT,
) -> Client:
    """
    Create a Client by loading cookies from a JSON file.

    Parameters
    ----------
    path : str
        Path to a JSON file containing the cookies dict.

    Example
    -------
    >>> client = await create_client_from_file("cookies.json")
    """
    with open(path, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    return await create_client(cookies, language, user_agent)


async def create_client_from_string(
    raw: str,
    language: str = 'en-US',
    user_agent: str = _DEFAULT_USER_AGENT,
) -> Client:
    """
    Create a Client from a raw cookie string copied from browser DevTools.

    How to get the string:
        1. Open https://x.com and log in
        2. DevTools (F12) → Network → any request → Headers → Cookie
        3. Copy the entire Cookie header value

    Parameters
    ----------
    raw : str
        e.g. ``"auth_token=abc123; ct0=xyz; twid=u%3D456"``

    Example
    -------
    >>> client = await create_client_from_string("auth_token=abc; ct0=xyz; twid=u%3D123")
    """
    return await create_client(_parse_cookie_string(raw), language, user_agent)


async def create_client_from_browser_export(
    data: 'list | str',
    language: str = 'en-US',
    user_agent: str = _DEFAULT_USER_AGENT,
) -> Client:
    """
    Create a Client from a browser cookie export (EditThisCookie / Cookie-Editor).

    How to get the export:
        1. Install EditThisCookie or Cookie-Editor browser extension
        2. Open https://x.com and log in
        3. Click the extension icon → Export → copies JSON to clipboard

    Parameters
    ----------
    data : list or str
        The JSON array (as a string or already parsed list).

    Example
    -------
    >>> raw = '[{"name":"auth_token","value":"abc","domain":".x.com",...}]'
    >>> client = await create_client_from_browser_export(raw)
    """
    if isinstance(data, str):
        data = json.loads(data)
    return await create_client(_parse_browser_export(data), language, user_agent)
