import os
import warnings

import pytest
import pytest_asyncio

from qqmusic_api import Credential
from qqmusic_api.album import Album
from qqmusic_api.mv import MV
from qqmusic_api.singer import Singer
from qqmusic_api.song import Song
from qqmusic_api.songlist import Songlist
from qqmusic_api.top import Top
from qqmusic_api.user import User, get_euin


@pytest_asyncio.fixture(scope="session")
async def credential():
    musicid = os.getenv("MUSIC_ID", 0)
    musickey = os.getenv("MUSIC_KEY", "")
    refresh_key = os.getenv("MUSIC_REFRESH_KEY", "")
    refresh_token = os.getenv("MUSIC_REFRESH_TOKEN", "")
    c = Credential(musicid=int(musicid), musickey=musickey, refresh_key=refresh_key, refresh_token=refresh_token)
    if not c.has_musicid() or not c.has_musickey():
        pytest.skip("未设置 MUSIC_ID 或 MUSIC_KEY")

    if not await c.can_refresh():
        os.environ["REFRESH"] = "true"
        warnings.warn("credential 不可刷新")
        pytest.skip("未设置 MUSIC_REFRESH_KEY 或 MUSIC_REFRESH_TOKEN")

    if await c.is_expired():
        await c.refresh()
        if await c.is_expired():
            warnings.warn("credential 已过期且刷新失败")
            pytest.skip("credential 已过期")

        github_env = os.getenv("GITHUB_ENV", None)
        if github_env is not None:
            with open(github_env, "a", encoding="utf8") as f:
                f.write(f"NEW_MUSIC_KEY={c.musickey}\n")
    return c


@pytest.fixture(scope="session")
def album():
    return Album(mid="000MkMni19ClKG")


@pytest.fixture(scope="session")
def mv():
    return MV("003HjRs318mRL2")


@pytest.fixture(scope="session")
def singer():
    return Singer("0025NhlN2yWrP4")


@pytest.fixture(scope="session")
def song():
    return Song(mid="004emQMs09Z1lz")


@pytest.fixture(scope="session")
def songlist():
    return Songlist(9069454203)


@pytest.fixture(scope="session")
def top():
    return Top(62)


@pytest_asyncio.fixture(scope="session")
async def user(credential):
    return User(await get_euin(credential.musicid), credential)
