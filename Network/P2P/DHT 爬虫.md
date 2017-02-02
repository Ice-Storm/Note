# DHT 爬虫
## DHT
DHT（Distributed Hash Table，分布式哈希表）。DHT 系统中有三个值，分别是节点标识（节点 ID），对象关键字（key）和对象值（value），节点存储的是对象的 \<key,value\> 对。

大部分结构式 P2P 网络都使用 DHT 系统。DHT 的主要功能包括3个内容：

- 标识符的生成和管理
- 提供重叠网络中的查询定位的路由服务
- 对提供的服务或文件的信息进行管理

DHT 系统有四个基本操作（以 Kademlia 算法为主）：

- ping 操作。作用是探测一个节点，用以判断该节点是否仍然在线。
- store 操作，作用是通知一个节点存储一个\<key,value\>对，以便以后查询需要。
- find_node 操作，作用是从自己的“路由表”对应的 K 桶中返回 k 个节点信息(IP address, UDP port, Node ID)给发送者。
- find_value 操作，作用是把 info-hash（key） 作为参数，如果本操作接收者正好存储了 info-hash 的 peers（value） 则返回 peers list，否则从自己的“路由表“中返回离 info-hash 更近的 k 个节点信息（同 find_node 过程）。

## Kademlia

DHT 系统有很多资源定位算法，包括 Chord，Pastry，CAN 和 Kademlia 等。其中 bittorrent 中的 DHT 系统选用了 Kademlia 算法作为资源定位算法。

Kademlia 与其他 DHT 算法相同，所有信息均以 \<key, value\> 对的散列表条目形式加以存储，这些 \<key, value\> 对分散地存储在各节点上。每个 ID 和关键字值有160bit。为了发布和寻找 \<key, value\> 对，Kademlia 采用两节点之间距离（Distance）的概念。与其他 DHT 算法相比，两节点距离不依靠物理距离、跳数，而是通过异或算法（XOR）为距离度量基础，建立了一个全新的 DHT 拓扑结果，大大提高了查询速度。

节点 X 要查找 ID 值为 t 的节点 T，过程如下：

1. 计算 X 到 T 的距离 $d(x, t) = x \oplus t$
2. 从 X 的第 [$log_2 d$]个 K 桶中取出 α 个节点的信息（各个实现 α 值不一样，有些是3有些则等于k值），同时进行 FIND_NODE 操作。如果这个K 桶中的信息少于 α 个，则从附近多个桶中选择距离最接近d 的总共α个节点。
3. 对接受到查询操作的每个节点，如果发现自己就是 T，则回答自己是最接近 T 的。否则测量自己和 T 的距离，并从自己对应的 K 桶中选择 α 个节点的信息给 X。
4. X 对新接受到的每个节点都再次执行 FIND_NODE 操作，此过程不断重复执行，直到每一个分支都有节点响应自己是最接近 T 的，或者说 FIND_NODE 操作返回的节点值没有都已经被查找过了，即找不到更近的节点了。
5. 通过上述查找操作，X 得到了 k 个最接近 T 的节点信息。

**注意**：这里用『最接近』这个说法，是因为 ID 值为t 的节点不一定存在网络中，也就是说 t 没有分配给任何一台电脑。

bt-dht 中查找 peers-list 的过程则换成 find_value 动作，但注意前文提到的区别即可以有类似的描述。

**注意**：Kademlia 算法运行一段时间后，大部分 \<key,value\> 对象会在节点 X 聚集，其中 X 的 ID 值和 key 的距离很近，也就是 Kademlia 算法查找资源的依据。

## DHT 爬虫协议

这里指的 DHT 爬虫主要是指使用 Kademlia 算法的 bt-dht 爬虫。bt-dht 使用 [krpc](http://www.bittorrent.org/beps/bep_0005.html) 协议和 [bencode](http://www.wikiwand.com/zh/Bencode) 编码。

bt-dht 请求有四种，分别是：

- ping（回复 pong)
- find_node（回复 found_node）
- get_peers（回复 got_peers）
- announce_peer

基本和 DHT 的四种基本操作一致，这里要介绍的是 announce_peer 请求，该请求表示节点 X 当前正在下载请求中指定的资源，发送的目标节点是之前向 X 发送过 got_peers 的节点，并且携带有 got_peers 中带有的 token 作为验证。bt-dht 爬虫主要搜集的就是 announce_peer 中携带的资源 info_hash 和 get_peers 中的资源 info_hash，可以以此了解资源的热度。

**注意**：got_peers 中返回的 peer 地址一般是 TCP 地址，返回的 node 地址是 UDP 地址。

## DHT 爬虫实现

在 Github 上已经有很多 DHT 爬虫的实现，简单列举几个我测试过的：

- [Fuck-You-GFW/simDHT](https://github.com/Fuck-You-GFW/simDHT)
- [wuzhenda/simDHT](https://github.com/wuzhenda/simDHT)
- [0x0d/dhtfck](https://github.com/0x0d/dhtfck)

其中两个 simDHT 都是真正的爬虫，而 dhtfck 更接近一个正常的 DHT 节点。不幸的是我一开始采用了 dhtfck 作为参考开发，即使开启了 32 个爬虫进行爬取，收到的 announce 数也寥寥无几。一度爬虫的开发陷入停滞，因为找不到提高爬虫效率的方法。对比网上博客介绍的爬虫效率，我只能无奈。直到发现了 simDHT，这个纯正的 DHT 爬虫。

对比了两个爬虫间的区别，我发现了问题的根源，dhtfck 每次只向数量很少的节点发出 find_node 请求，并一直维护 node 池中的节点，导致最终爬虫只被少数节点记录，收集效率当然不高。而 simDHT 则是以一定频率按顺序向节点列表中的节点发出 find_node 请求，并删除旧的节点，这样发现该爬虫的节点以很快的速度增长，而且不需要定期维护节点池。

### 提高爬虫效率的几个关键点

- 向所有已知节点发送 find_node 请求。
- find_node 请求中的 id 值为随机指或已知其他 node 的值，这样一个爬虫就可以伪装成很多个节点，收到更多消息。
- find_node 请求中的 taget 值为随机，不要指定为本节点的 id 值，因为这样的话收到的节点ID 范围就会遇到瓶颈，无法收到范围更广的节点。
- 最重要的是实现 find_node, process_find_node_response, process_get_peers_request, process_announce_peer_request 四个方法。ping，pong 之类的不实现不影响工作。
- 爬虫有时会一直搜不到数据，这时可能是爬虫 BootStrap 失败，几个 router 站点暂时屏蔽了本 ip 或者没有还开启，需要进一步调试确定。

**注意**：DHT 爬虫和 DHT 节点并不完全一样，DHT 爬虫只关心让更多的节点发现自己，并不关心自己记得多少节点（感觉这爬虫混在 DHT 节点中有点破坏 DHT 系统的稳定性）。

获取了 info_hash 后可以从一些种子网站下取对应的种子，如 [torcache](http://torcache.net/)；也可以构造磁力链接然后用迅雷等工具下载；也可以借助 libtorrent 库下载内容，甚至借助 bittorrent 协议中的 [Extension for Peers to Send Metadata Files](http://www.bittorrent.org/beps/bep_0009.html)，通过发出 announce_peer 的节点获取资源。

在获取 ip 时会出现一个怪现象，有时获取到的不同 ip 数保持在1261个左右，这时无法收到任何或者极少 announce，爬虫工作不正常，只有突破这个个数到达10000以上时，才开始接收 announce。**怀疑是 ip 队列中消费者消耗速度慢，一直满员，导致新的外围 ip 进不去，一直在这1261个 ip 范围内打转，考虑使用异步 io 提高效率。**。

提高 io 效率和队列容量到20000后，成功解决问题，说明之前对队列太满的判断是正确的。(但是有时也会在队列没满就只能到达1261的情况)

## 获取种子信息

```python
# 建立 TCP 连接，交换协议头
self.transport.write(
         b'\x13BitTorrent protocol'
         b'\x00\x00\x00\x00\x00\x10\x00\x04' + \
         self.infohash + self.peerid
        )

 # 种子扩展协议 handshake
 extended_handshake = bencode({
                'm': {b'ut_metadata': 2},
                'v': 'S.P.E.W.'
            })
 self.write_extended_message(0, extended_handshake)
 
 def write_extended_message(self, ex_type, msg):
     self.write_message(20, bytes([ex_type]) + msg)
     
 def write_message(self, type, msg):
     msg_len = 1 + len(msg)
     self.transport.write(msg_len.to_bytes(length=4, byteorder='big') + \
                          bytes([type]) + msg)
 ```
## 常见错误
bdecode 解压错误：从 peer 获取的 metadata 解压错误，这有可能是由于接收超时导致 metadata 数据不完整，最后的 pieces 部分长度不符合要求，目前的 workaround 是删除 pieces 部分。

当全部使用 eventlet.greenthread 代替 Thread 后，效率并没有提升，因为 greenthread 并不会主动放弃 cpu。（如何组合爬虫的工作效率最高？）

## 蜜罐系统
DHT 网络有蜜罐系统。

## 参考资料

- [写了个磁力搜索的网页](http://xiaoxia.org/2013/05/11/magnet-search-engine/)
- [搜片神器](http://www.cnblogs.com/miao31/p/3332819.html)
- [BitTorrent DHT 协议中文翻译](http://justjavac.com/other/2015/02/01/bittorrent-dht-protocol.html)
- [The BitTorrent Protocol Specification](http://www.bittorrent.org/beps/bep_0003.html)
- [DHT Protocol](http://www.bittorrent.org/beps/bep_0005.html)
- [Extension for Peers to Send Metadata Files](http://www.bittorrent.org/beps/bep_0009.html)
- [Extension Protocol](http://www.bittorrent.org/beps/bep_0010.html)
 



