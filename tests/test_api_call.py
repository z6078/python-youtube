import json
import unittest
import pyyoutube

import responses


class TestApiCall(unittest.TestCase):
    BASE_URL = "https://www.googleapis.com/youtube/v3/"

    def setUp(self):
        self.base_path = "testdata/"
        self.api = pyyoutube.Api(client_id="xx", client_secret="xx", api_key="xx")

    @responses.activate
    def testGetPlaylistItems(self):
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_playlist_item(parts=[])
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_playlist_item(
                playlist_id="PLOU2XLYxmsIJpufeMHncnQvFOe0K3MhVp", parts="id,part"
            )
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_playlist_item(
                playlist_id="PLOU2XLYxmsIJpufeMHncnQvFOe0K3MhVp",
                playlist_item_id="UExPVTJYTFl4bXNJSkpWbkhXbWQxcWZyMENhcTRWWkN1NC4zRjM0MkVCRTg0MkYyQTM0",
            )
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_playlist_item()
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.MISSING_PARAMS
            )

        with open(f"{self.base_path}playlist_items_info.json") as f:
            res_data_1 = f.read()
        with open(f"{self.base_path}playlist_items_info_next.json") as f:
            res_data_2 = f.read()
        responses.add(
            responses.GET, self.BASE_URL + "playlistItems", body=res_data_1, status=200
        )
        responses.add(
            responses.GET, self.BASE_URL + "playlistItems", body=res_data_2, status=200
        )
        playlist_items, summary = self.api.get_playlist_item(
            playlist_id="PLOU2XLYxmsIJJVnHWmd1qfr0Caq4VZCu4", count=10,
        )
        self.assertEqual(len(playlist_items), 5)
        self.assertEqual(
            playlist_items[0].id,
            "UExPVTJYTFl4bXNJSkpWbkhXbWQxcWZyMENhcTRWWkN1NC4zRjM0MkVCRTg0MkYyQTM0",
        )
        self.assertEqual(summary["totalResults"], 23)

        playlist_items, summary = self.api.get_playlist_item(
            playlist_item_id="UExPVTJYTFl4bXNJSkpWbkhXbWQxcWZyMENhcTRWWkN1NC4xMkVGQjNCMUM1N0RFNEUx",
            return_json=True,
            video_id="CqkuGBpZ_q0",
        )
        self.assertEqual(
            playlist_items[0]["id"],
            "UExPVTJYTFl4bXNJSkpWbkhXbWQxcWZyMENhcTRWWkN1NC4xMkVGQjNCMUM1N0RFNEUx",
        )

    @responses.activate
    def testGetVideoById(self):
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_video_by_id()
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.MISSING_PARAMS
            )
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_video_by_id(parts=[])
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_video_by_id(video_id="Ks-_Mh1QhMc", parts="id,part")
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )
        with open(f"{self.base_path}video_info.json") as f:
            videos_data_by_id = f.read()
        responses.add(
            responses.GET, self.BASE_URL + "videos", body=videos_data_by_id, status=200
        )
        res = self.api.get_video_by_id(video_id="Ks-_Mh1QhMc")
        self.assertEqual(res[0].id, "D-lhorsDlUQ")
        self.assertEqual(res[0].statistics.viewCount, "7920")

        res = self.api.get_video_by_id(video_id="Ks-_Mh1QhMc", return_json=True)
        self.assertEqual(res[0]["id"], "D-lhorsDlUQ")

    @responses.activate
    def testGetVideosByFilter(self):
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_video_by_filter()
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.MISSING_PARAMS
            )
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_video_by_filter(parts=[])
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_video_by_filter(chart="mostPopular", parts="id,part")
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )

        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_video_by_filter(chart="mostPopular", my_rating="like")
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )

        with open(f"{self.base_path}videos_info.json") as f:
            videos_data_by_filter = f.read()
        responses.add(
            responses.GET,
            self.BASE_URL + "videos",
            body=videos_data_by_filter,
            status=200,
        )
        with open(f"{self.base_path}videos_info_next.json") as f:
            videos_data_by_filter = f.read()
        responses.add(
            responses.GET,
            self.BASE_URL + "videos",
            body=videos_data_by_filter,
            status=200,
        )
        res, summary = self.api.get_video_by_filter(
            chart="mostPopular", category_id=17, count=10
        )
        self.assertEqual(len(res), 5)
        self.assertEqual(res[0].id, "9wCvNsXREls")

        res, summary = self.api.get_video_by_filter(
            chart="mostPopular", region_code="US", count=8
        )
        self.assertEqual(len(res), 8)

        res, summary = self.api.get_video_by_filter(
            my_rating="dislike", return_json=True
        )
        self.assertEqual(len(res), 5)

    @responses.activate
    def testGetCommentThreads(self) -> None:
        with open(f"{self.base_path}comment_threads_by_all_to_channel_id.json") as f:
            res_data_by_all = f.read()
        with open(f"{self.base_path}comment_threads_by_video_id.json") as f:
            res_data_by_video = f.read()
        responses.add(
            responses.GET,
            self.BASE_URL + "commentThreads",
            body=res_data_by_all,
            status=200,
        )
        responses.add(
            responses.GET,
            self.BASE_URL + "commentThreads",
            body=res_data_by_video,
            status=200,
        )
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_comment_threads()
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_comment_threads(channel_id="channel id", order="rev")
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_comment_threads(parts=[])
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_comment_threads(channel_id="channel id", parts="id,part")
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )

        comment_threads = self.api.get_comment_threads(
            all_to_channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw", count=4, search_term="",
        )
        self.assertEqual(len(comment_threads), 4)
        self.assertEqual(comment_threads[0].id, "UgzhytyP79_PwaDd4UB4AaABAg")

        comment_threads_by_video = self.api.get_comment_threads(
            video_id="D-lhorsDlUQ", return_json=True
        )
        self.assertEqual(len(comment_threads_by_video), 5)
        self.assertEqual(
            comment_threads_by_video[0]["id"], "UgydxWWoeA7F1OdqypJ4AaABAg"
        )

    @responses.activate
    def testGetCommentThreadInfo(self) -> None:
        with open(f"{self.base_path}comment_threads_by_id.json") as f:
            res_data = f.read()
        responses.add(
            responses.GET, self.BASE_URL + "commentThreads", body=res_data, status=200
        )

        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_comment_thread_info()
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_comment_thread_info(parts=[])
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_comment_thread_info(
                comment_thread_id="Ugz097FRhsQy5CVhAjp4AaABAg", parts="id,part"
            )
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )

        comment_threads = self.api.get_comment_thread_info(
            comment_thread_id="Ugz097FRhsQy5CVhAjp4AaABAg,UgzhytyP79_PwaDd4UB4AaABAg"
        )
        self.assertEqual(len(comment_threads), 2)

        comment_threads = self.api.get_comment_thread_info(
            "Ugz097FRhsQy5CVhAjp4AaABAg,UgzhytyP79_PwaDd4UB4AaABAg", return_json=True
        )
        self.assertEqual(comment_threads[0]["id"], "Ugz097FRhsQy5CVhAjp4AaABAg")

    @responses.activate
    def testGetCommentsByParent(self) -> None:
        with open(f"{self.base_path}comments_by_parent_id.json") as f:
            res_data_by_parent = f.read()
        responses.add(
            responses.GET,
            self.BASE_URL + "comments",
            body=res_data_by_parent,
            status=200,
        )

        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_comments_by_parent()
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_comments_by_parent(parts=[])
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_comments_by_parent(
                parent_id="UgwYjZXfNCUTKPq9CZp4AaABAg", parts="id,part"
            )
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )

        comments = self.api.get_comments_by_parent(
            parent_id="UgwYjZXfNCUTKPq9CZp4AaABAg", count=1
        )
        self.assertEqual(len(comments), 1)

        comments = self.api.get_comments_by_parent(
            parent_id="UgwYjZXfNCUTKPq9CZp4AaABAg", return_json=True
        )
        self.assertEqual(
            comments[0]["id"], "UgwYjZXfNCUTKPq9CZp4AaABAg.8yxhlQJogG18yz_cXK9Kcj"
        )

    @responses.activate
    def testGetCommentInfo(self) -> None:
        with open(f"{self.base_path}comments_by_id.json") as f:
            res_data_by_id = f.read()
        responses.add(
            responses.GET, self.BASE_URL + "comments", body=res_data_by_id, status=200
        )
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_comment_info()
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_comment_info(parts=[])
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_comment_info(
                comment_id="UgxKREWxIgDrw8w2e_Z4AaABAg", parts="id,part"
            )
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )

        comments = self.api.get_comment_info(
            comment_id="UgxKREWxIgDrw8w2e_Z4AaABAg,UgyrVQaFfEdvaSzstj14AaABAg"
        )
        self.assertEqual(len(comments), 2)
        comments = self.api.get_comment_info(
            comment_id="UgxKREWxIgDrw8w2e_Z4AaABAg,UgyrVQaFfEdvaSzstj14AaABAg",
            return_json=True,
        )
        self.assertEqual(comments[0]["id"], "UgxKREWxIgDrw8w2e_Z4AaABAg")

    @responses.activate
    def testGetVideoCategory(self) -> None:
        with open(f"{self.base_path}video_categories_info_by_id.json") as f:
            video_categories_by_id = json.loads(f.read().encode("utf-8"))
        with open(f"{self.base_path}video_categories_info_by_region.json") as f:
            video_categories_by_region = json.loads(f.read().encode("utf-8"))
        responses.add(
            responses.GET,
            self.BASE_URL + "videoCategories",
            json=video_categories_by_id,
            status=200,
        )
        responses.add(
            responses.GET,
            self.BASE_URL + "videoCategories",
            json=video_categories_by_region,
            status=200,
        )

        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_video_categories()
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_video_categories(category_id="1", region_code="US")
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_video_categories(parts=[])
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_video_categories(category_id="1", parts="id,part")
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )

        video_categories = self.api.get_video_categories(category_id="1,2", hl="zh_CN")
        self.assertEqual(video_categories[1].snippet.title, "汽车")
        video_categories = self.api.get_video_categories(
            region_code="US", return_json=True
        )
        self.assertEqual(len(video_categories), 32)

    @responses.activate
    def testGetGuideCategory(self) -> None:
        with open(f"{self.base_path}guide_categories_by_id.json") as f:
            guide_categories_by_id = json.loads(f.read().encode("utf-8"))
        with open(f"{self.base_path}guide_categories_by_region.json") as f:
            guide_categories_by_region = json.loads(f.read().encode("utf-8"))
        responses.add(
            responses.GET,
            self.BASE_URL + "guideCategories",
            json=guide_categories_by_id,
            status=200,
        )
        responses.add(
            responses.GET,
            self.BASE_URL + "guideCategories",
            json=guide_categories_by_region,
            status=200,
        )

        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_guide_categories()
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_guide_categories(category_id="GCQ29tZWR5", region_code="US")
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_guide_categories(parts=[])
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )
        with self.assertRaises(pyyoutube.PyYouTubeException) as ex:
            self.api.get_guide_categories(category_id="GCQ29tZWR5", parts="id,part")
            self.assertEqual(
                ex.exception.status_code, pyyoutube.error.ErrorCode.INVALID_PARAMS
            )

        guide_categories = self.api.get_guide_categories(
            category_id="GCQ29tZWR5,GCTXVzaWM", hl="zh_CN"
        )
        self.assertEqual(guide_categories[1].snippet.title, "音乐")
        guide_categories = self.api.get_guide_categories(
            region_code="US", return_json=True
        )
        self.assertEqual(len(guide_categories), 11)
