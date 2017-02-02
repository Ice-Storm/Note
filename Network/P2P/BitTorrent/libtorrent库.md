# libtorrent库
libtorrent 库一般是指 rasterbar 版本，并且编译时可以指定 python-binding。

**注意**：最新版的 libtorrent 一般不是很稳定，会出各种奇怪的问题，可以使用稍旧一点的版本。

## add_torrent_params

The add_torrent_params is a parameter pack for adding torrents to a session. The key fields when adding a torrent are:

- ti - when you have a .torrent file
- url - when you have a magnet link or http URL to the .torrent file
- info_hash - when all you have is an info-hash (this is similar to a magnet link)

If you only specify the info-hash, the torrent file will be downloaded from peers, which requires them to support the metadata extension. For the metadata extension to work, libtorrent must be built with extensions enabled (TORRENT_DISABLE_EXTENSIONS must not be defined). It also takes an optional name argument. This may be left empty in case no name should be assigned to the torrent. In case it's not, the name is used for the torrent as long as it doesn't have metadata. See torrent_handle::name.

```cpp

```

