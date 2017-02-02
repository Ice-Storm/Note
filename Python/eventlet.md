# 
eventlet 调用 spawn 后立即返回，并不会立即调用函数，而是会等待下一次时机，比如出现 eventlet 模块中的阻塞调用。

