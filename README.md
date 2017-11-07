#itemprofile服务说明
itemprofile服务主要用来取得召回商品的属性数据, 商品的数据被分为不同部分, 分别存放在不同的地方. 取数据时, 异步地从不同的地方不同的数据, 最后再拼接到一起.

## 此模块的类图

![pic_itemprofle](./pic_itemprofle.png)

## ItemPropertyDataBlock
ItemPropertyDataBlock是一个抽象类, 有一个mergeData()的虚函数, 它派生出PredictorEmbeddingWrapper, PredictorFeedbackWrapper等具体的类. 这些类会具体实现自己的mergeData()函数, 来把自己的数据填充到商品属性列表里. 它们一般会根据一个dataMap进行初始化.
## Fetcher
Fetcher<K, V, C, R>是一个模板类, 虚函数buildReq()用于设置请求, callClient()用于请求服务, 得到数据, 成员方法getData()并行地完成取数据的功能, 每次会取BATCHSIZE个数据, 最后进行数据的拼接. 每次取数前, 都会调用一次buildReq()构建请求, 调用一次callClient()得到请求数据.

Fetcher<K, V, C, R>派生出PredictorMutiGetFetcher, PredictorMutiModelFetcher等具体的类, 实现了不同格式的取数方式.

##SkuPropertyFetcher
SkuPropertyFetcher类实际上和Fetcher<K, V, C, R>并不存在继承和派生的关系, 可以认为是管理很多具体的fetcher的manage类. 它的接口函数实现了不同的部分数据的取数功能, 如getFeedbackPredictorData(), getEmbeddingPredictorData(). 这些函数在具体取数据的时候, 会接收一个对应的cache实例, 使用一个对应的fetcher实例(SkuPropertyFetcher在初始化的时候会生成一些fetcher实例), 从缓存或服务端取数据, 返回一个ItemPropertyDataBlock实例. 下面说明getFeedbackPredictorData()函数的其工作流程.
```c++
void SkuPropertyFetcher::getFeedbackPredictorData(LruCache, ...){
    从cache中取相应skus的数据  // 这里的cache是从参数传入的.
    // this->skuFeedbackPredictorFetcher的类型为std::unique_ptr<PredictorMutiModelFetcher>, 会在SkuPropertyFetcher初始化的时候进行初始化.
    从服务里取得其它没命中cache的数据. this->skuFeedbackPredictorFetcher->getData(miss_skus, fetcherResult, location)
    更新cache
    利用两部分数据, 生成一个ItemPropertyDataBlock对象. 设置给response.
        std::unique_ptr<ItemPropertyDataBlock> dataPtr(new PredictorFeedbackWrapper(std::move(*cacheResult)));
        res->setValue(std::move(dataPtr));
}
```

## ItemProfileService
ItemProfileService是服务的入口,  首先会掉用init()方法, 初始化不同的cache和组件skuPropertyFetcher. 如
```c++
std::unique_ptr<SkuPropertyFetcher> skuPropertyFetcher;
std::unique_ptr<LruCache<std::string, std::shared_ptr<std::vector<double>> > >
	feedbackPredictorCache;
std::unique_ptr<LruCache<std::string, std::shared_ptr<std::vector<double>> > >
	embeddingPredictorCache;
```

ItemProfileService的主要接口函数是acceptRequest(), 它会调用getSkuPropertys(items, req, res)函数来填充商品的数据, 得到相应的response.

ItemProfileService::getSkuPropertys()函数是整个服务的重点, 它完成了整个取数据和合并数据的工作.  该函数会利用相应的cache和skuPropertyFetcher属性中的对应方法取得不同的DataBlock,  然后遍历DataBlock列表, 用其mergeData()函数进行商品属性的合并. 其中取数的过程是并行进行的, 不同部分的数据一一对应一个cache和skuPropertyFetcher中的一个方法.如:

```c++
// skuPropertyFetcher->getFeedbackPredictorData ()
// 对应的cache为 feedbackPredictorCache
auto promPredictorResult = std::make_shared<folly::Promise<std::unique_ptr<ItemPropertyDataBlock>>>();
skuPropertyFetcher->getFeedbackPredictorData(skus, 
    promPredictorResult, 
    feedbackPredictorCache.get(),
    config->cache.useCache, location);
futureVec.push_back(promPredictorResult->getFuture());

// skuPropertyFetcher->getEmbeddingPredictorData 
// 对应的cache为embeddingPredictorCache
auto promEmbeddingResult = std::make_shared<folly::Promise<std::unique_ptr<ItemPropertyDataBlock>>>();
skuPropertyFetcher->getEmbeddingPredictorData(skus,
    promEmbeddingResult,
    embeddingPredictorCache.get(),
    config->cache.useCache, location);
futureVec.push_back(promEmbeddingResult->getFuture());
```
