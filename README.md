# filter服务说明

filter服务是在取得商品属性数据之后, 对商品进行过滤的服务. 可以配置不同的过滤插件, 过滤不同条件的商品.

## 类图

![filter](./pic_filter.png)

## Filter

Filter类是一个抽象类,  其派生了不同的类如BrandFilter, TitleFilter, 用于实现不同的过滤.

Filter类的过滤是由`DoFilter(const FilterParam& filterParam,const FilterContext& filter_context, ItemPropertiesPtr& items)` 函数完成的, 根据接收的参数不同, 对items进行过滤, 结果仍然保存在items里.

Filter类另外还有个函数getItemProfileFlags(), 返回一个ItemProfileFlags::FlagSet对象.


## FilterManager

- filters_: `std::map<std::string,std::shared_ptr<Filter> >`

  filters的map字典, key为filter的名字, value为生成的实例对象的指针.
- bool init(&config)

  根据配置初始化config, context_属性
- void Register(&name, &filter)
  注册Filter插件, 加入到filter_私有属性这个map字典里.这个函数用宏包装了一下, 在每个Filter的cpp里完成注册.
- void DoFilter(&filterParam, &items)
  主要的接口函数. 首先会调用preFilter()函数把items商品标记是否是通过无序召回的. 然后通过请求的predictId, 得到与之对应的Filter列表, 进行过滤(利用不同Filter实例的DoFilter()函数.), 过滤的结果原地址存放.
- void PreFilter(&request, &items)
  根据request中的recall_list每个RecallItem, 依次MarkDownUnorderdRecallFlag(sku, &items)标记items是否是通过无序召回的.
- MarkDownUnorderdRecallFlag(sku, &items)
  遍历items, 把itemId == sku的商品标记为 skuData.isFromUnorderdRecallSrc = true
