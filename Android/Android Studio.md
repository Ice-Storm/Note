Android Studio
==============


# Error

## 虚拟化错误

	emulator: Failed to sync vcpu reg
	emulator: Failed to sync HAX vcpu context

你可能有其它要用到虚拟化的程序在运行，比如virtual box或vmware，关掉再试。

## Gradle错误
	
	Gradle: Resolve dependencies ':app_debugCompile' 卡死

if you are using proxy, it seems https proxy server setting is not correctly done in Android studio 1.3. You can set https proxy server manually in gradle.properties,

systemProp.https.proxyHost=proxy.server.address
systemProp.https.proxyPort=8080
see Gradle Sync fails in Android studio 1.3 and gradle behind proxy in Android Studio 1.3. 简而言之，在 gradle 中也要设置 httpproxy 或者开全局系统代理。