"""专辑相关 API"""

from typing import Optional

from .utils.network import Api
from .utils.utils import get_api

API = get_api("album")


class Album:
    """专辑类

    Attributes:
        mid: 专辑 mid
        id:  专辑 id
    """

    def __init__(
        self,
        *,
        mid: Optional[str] = None,
        id: Optional[int] = None,
    ):
        """初始化专辑类

        Note:
            歌曲 mid 和 id，两者至少提供一个

        Args:
            mid: 专辑 mid
            id:  专辑 id
        """
        if mid is None and id is None:
            raise ValueError("mid or id must be provided")
        self.mid = mid or ""
        self.id = id or 0
        self._info: Optional[dict] = None

    async def get_mid(self) -> str:
        """获取专辑 mid

        Returns:
            专辑 mid
        """
        if not self.mid:
            self.mid = (await self.get_detail())["basicInfo"]["albumMid"]
        return self.mid

    async def get_id(self) -> int:
        """获取专辑 id

        Returns:
            专辑 id
        """
        if not self.id:
            self.id = (await self.get_detail())["basicInfo"]["albumID"]
        return self.id

    async def get_detail(self) -> dict:
        """获取专辑详细信息

        Returns:
            专辑详细信息
        """
        if not self._info:
            self._info = await Api(**API["detail"]).update_params(albumMid=self.mid, albumId=self.id).result
        return self._info

    async def get_song(self) -> list[dict]:
        """获取专辑歌曲

        Returns:
            歌曲列表
        """
        result = await Api(**API["song"]).update_params(albumMid=self.mid, albumId=self.id, begin=0, num=0).result
        return [song["songInfo"] for song in result["songList"]]
