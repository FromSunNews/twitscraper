# Rate Limits

**All limits reset every 15 minutes.**

`-` means no documented per-15min limit (may still have daily account-level limits).

| Function                              | Limit / 15min | Endpoint                            |
|---------------------------------------|---------------|-------------------------------------|
| `search_tweet`, `search_user`         | 50            | SearchTimeline                      |
| `get_tweet_by_id`                     | 150           | TweetDetail                         |
| `get_timeline`                        | 500           | HomeTimeline                        |
| `get_latest_timeline`                 | 500           | HomeLatestTimeline                  |
| `get_trends`                          | 20,000        | guide.json                          |
| `get_user_by_screen_name`             | 95            | UserByScreenName                    |
| `get_user_by_id`                      | 500           | UserByRestId                        |
| `get_user_tweets` (Tweets)            | 50            | UserTweets                          |
| `get_user_tweets` (Replies)           | 50            | UserTweetsAndReplies                |
| `get_user_tweets` (Media)             | 500           | UserMedia                           |
| `get_user_tweets` (Likes)             | 500           | Likes                               |
| `get_user_followers`                  | 50            | Followers                           |
| `get_user_following`                  | 500           | Following                           |
| `get_user_verified_followers`         | 500           | BlueVerifiedFollowers               |
| `get_user_followers_you_know`         | 500           | FollowersYouKnow                    |
| `get_bookmarks`                       | 500           | Bookmarks                           |
| `get_favoriters`                      | 500           | Favoriters                          |
| `get_retweeters`                      | 500           | Retweeters                          |
| `get_scheduled_tweets`                | 500           | FetchScheduledTweets                |
| `get_list`                            | 500           | ListByRestId                        |
| `get_list_tweets`                     | 500           | ListLatestTweetsTimeline            |
| `get_lists`                           | 500           | ListsManagementPageTimeline         |
| `get_list_members`                    | 500           | ListMembers                         |
| `get_list_subscribers`                | 500           | ListSubscribers                     |
| `get_notifications` (All)             | 180           | notifications/all.json              |
| `get_notifications` (Mentions)        | 180           | notifications/mentions.json         |
| `get_notifications` (Verified)        | 180           | notifications/verified.json         |
| `get_dm_history`, `get_group_dm_history` | 900        | conversation/{id}.json              |
| `get_user_subscriptions`              | 500           | UserCreatorSubscriptions            |
| `follow_user`                         | 15            | friendships/create.json             |
| `unfollow_user`                       | 187           | friendships/destroy.json            |
| `block_user`                          | 187           | blocks/create.json                  |
| `unblock_user`                        | 187           | blocks/destroy.json                 |
| `mute_user`                           | 187           | mutes/users/create.json             |
| `unmute_user`                         | 187           | mutes/users/destroy.json            |
| `send_dm`                             | 187           | dm/new2.json                        |
| `logout`                              | 187           | account/logout.json                 |
| `login`                               | 187           | onboarding/task.json                |
| `create_tweet`                        | -             | CreateTweet                         |
| `delete_tweet`                        | -             | DeleteTweet                         |
| `retweet`                             | -             | CreateRetweet                       |
| `delete_retweet`                      | -             | DeleteRetweet                       |
| `favorite_tweet`                      | -             | FavoriteTweet                       |
| `unfavorite_tweet`                    | -             | UnfavoriteTweet                     |
| `bookmark_tweet`                      | -             | CreateBookmark                      |
| `delete_bookmark`                     | -             | DeleteBookmark                      |
| `delete_all_bookmarks`                | -             | BookmarksAllDelete                  |
| `create_poll`                         | -             | cards/create.json                   |
| `vote`                                | -             | capi/passthrough/1                  |
| `upload_media`                        | -             | media/upload.json                   |
| `create_scheduled_tweet`              | -             | CreateScheduledTweet                |
| `delete_scheduled_tweet`              | -             | DeleteScheduledTweet                |
| `send_dm`                             | 187           | dm/new2.json                        |
| `delete_dm`                           | -             | DMMessageDeleteMutation             |
| `add_reaction_to_message`             | -             | useDMReactionMutationAddMutation    |
| `remove_reaction_from_message`        | -             | useDMReactionMutationRemoveMutation |
| `create_list`                         | -             | CreateList                          |
| `edit_list`                           | -             | UpdateList                          |
| `add_list_member`                     | -             | ListAddMember                       |
| `remove_list_member`                  | -             | ListRemoveMember                    |
| `add_members_to_group`                | -             | AddParticipantsMutation             |
| `change_group_name`                   | 900           | {GroupID}/update_name.json          |
