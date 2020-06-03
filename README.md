# python微服务框架之nameko实践

---
## 相关内容，欢迎关注微信公众号：数据分析师成长之路

---
# 本篇大纲

主要对应五个示例，循序渐进的方式来实践nameko相关内容。

## 示例一：flask + nameko + rabbitMQ + 单模块 + 临时性建立rpc通道

	1、通过nameko管理微服务。
	2、通过flask部署发布服务，flask中会封装调用微服务。

## 示例二：flask + nameko + rabbitMQ + swagger + 单模块 + 临时性建立rpc通道

    1、通过nameko管理微服务。
	2、通过flask部署发布服务，flask中会封装调用微服务。
	3、swagger管理api文档说明可视化。

## 示例三：flask + nameko + rabbitMQ + swagger + 单模块 + 永久性建立rpc通道

    1、nameko管理微服务。
	2、flask发布服务，flask中会封装调用微服务。
	3、swagger管理api文档说明可视化。

## 示例四：flask + nameko + rabbitMQ + swagger + 多模块 + 永久性建立rpc通道

    1、通过nameko向rabbitmq注册多个微服务。
    2、不同模块组成的微服务之间进行彼此间的通信。
	3、flask最终对外发布服务，并调用nameko管理微服务。
	4、swagger进行api文档可视化。

## 示例五：flask + nameko + rabbitMQ + swagger + 多模块 + 永久性建立rpc通道 + 订阅发布模式

    1、发布多个微服务，实现订阅发布的模式。
	2、发布方给订阅方数据，订阅方接收到数据后做相应的处理。
	3、发布方数据生成有两种方式，一种是定时生成数据，进行发布，另一种是从服务接收数据，进行发布。
	4、订阅者一旦发现有数据，立即进行消费，并存储结果。
	5、Web端实现两个接口，一个是直接获取最新的自动产生的结果。
	6、另一个是主动传输数据给发布方，并从对应的订阅方获取结果。
