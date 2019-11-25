"""
    These are playlistItem related models.
"""

from dataclasses import dataclass, field
from typing import Optional

from .base import BaseModel
from .mixins import DatetimeTimeMixin
from .common import BaseResource, Thumbnails


@dataclass
class PlaylistItemContentDetails(BaseModel, DatetimeTimeMixin):
    """
    A class representing the playlist item's content details info.

    Refer: https://developers.google.com/youtube/v3/docs/playlistItems#contentDetails
    """

    videoId: Optional[str] = field(default=None)
    note: Optional[str] = field(default=None, repr=False)
    videoPublishedAt: Optional[str] = field(default=None)


@dataclass
class ResourceId(BaseModel):
    """
    A class representing the playlist item's snippet resource info.

    Refer: https://developers.google.com/youtube/v3/docs/playlistItems#snippet.resourceId
    """

    kind: Optional[str] = field(default=None)
    videoId: Optional[str] = field(default=None)


@dataclass
class PlaylistItemSnippet(BaseModel, DatetimeTimeMixin):
    """
    A class representing the playlist item's snippet info.

    Refer: https://developers.google.com/youtube/v3/docs/playlistItems#snippet
    """

    publishedAt: Optional[str] = field(default=None, repr=False)
    channelId: Optional[str] = field(default=None, repr=False)
    title: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    thumbnails: Optional[Thumbnails] = field(default=None, repr=False)
    channelTitle: Optional[str] = field(default=None, repr=False)
    playlistId: Optional[str] = field(default=None, repr=False)
    position: Optional[int] = field(default=None, repr=False)
    resourceId: Optional[ResourceId] = field(default=None, repr=False)


@dataclass
class PlaylistItemStatus(BaseModel):
    """
    A class representing the playlist item's status info.

    Refer: https://developers.google.com/youtube/v3/docs/playlistItems#status
    """

    privacyStatus: Optional[str] = field(default=None)


@dataclass
class PlaylistItem(BaseResource):
    """
    A class representing the playlist item's info.

    Refer: https://developers.google.com/youtube/v3/docs/playlistItems
    """

    snippet: Optional[PlaylistItemSnippet] = field(default=None, repr=False)
    contentDetails: Optional[PlaylistItemContentDetails] = field(
        default=None, repr=False
    )
    status: Optional[PlaylistItemStatus] = field(default=None, repr=False)