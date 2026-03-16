# 茶叶领域本体 (Tea Ontology)

## 1. 概述

本本体定义了茶叶领域的核心概念、分类体系、属性和关系，为知识图谱构建和语义推理提供标准化模型。

**命名空间**: `tea-ontology`
**版本**: 1.0.0
**创建日期**: 2026-03-16

---

## 2. 核心类 (Core Classes)

### 2.1 茶叶 (TeaLeaf)

**定义**: 茶树的嫩叶，经过适当加工后可制成饮用茶制品。

**子类**:
- 绿茶 (GreenTea)
- 白茶 (WhiteTea)
- 黄茶 (YellowTea)
- 青茶/乌龙茶 (OolongTea)
- 红茶 (BlackTea)
- 黑茶 (DarkTea)
- 再加工茶 (RefinedTea)

**属性**:
- `hasOrigin`: 产地 (引用: TeaRegion)
- `hasCultivar`: 茶树品种 (引用: TeaCultivar)
- `hasPluckingStandard`: 采摘标准 (枚举: 单芽/一芽一叶/一芽二叶/一芽三叶)
- `hasHarvestSeason`: 采摘季节 (枚举: 春茶/夏茶/秋茶/冬茶)
- `hasProcessingMethod`: 加工工艺 (引用: TeaProcessing)
- `hasGrade`: 等级 (枚举: 特级/一级/二级/三级/四级)
- `hasMoistureContent`: 含水量 (百分比)
- `hasPrice`: 价格 (货币类型: 人民币/斤)
- `hasShelfLife`: 保质期 (数值类型: 月)

---

### 2.2 绿茶 (GreenTea)

**定义**: 不发酵茶，经杀青、揉捻、干燥等工艺制成。

**特征**:
- 发酵程度: 0%
- 茶汤颜色: 绿叶清汤
- 口感: 鲜爽回甘
- 茶多酚含量: 高

**子类**:
- 炒青绿茶 (Pan-FiredGreenTea)
- 蒸青绿茶 (SteamedGreenTea)
- 烘青绿茶 (BakedGreenTea)
- 晒青绿茶 (Sun-DriedGreenTea)

**著名品种**:
- 西湖龙井 (WestLakeLongjing)
- 碧螺春 (BiLuoChun)
- 黄山毛峰 (HuangshanMaofeng)
- 太平猴魁 (TaipingHoukui)
- 安吉白茶 (AnjiBaiCha)
- 竹叶青 (ZhuYeQing)
- 恩施玉露 (EnshiYulu)
- 六安瓜片 (LiuAnGuaPian)

---

### 2.3 白茶 (WhiteTea)

**定义**: 轻微发酵茶，经萎凋、干燥制成。

**特征**:
- 发酵程度: 5%-10%
- 茶汤颜色: 浅杏黄
- 口感: 清淡甘甜
- 储存特性: 越陈越香

**子类**:
- 白毫银针 (BaiHaoYinZhen)
- 白牡丹 (BaiMuDan)
- 贡眉 (GongMei)
- 寿眉 (ShouMei)

**著名产地**:
- 福建福鼎 (Fuding)
- 福建政和 (Zhenghe)
- 云南景谷 (Jinggu)

---

### 2.4 黄茶 (YellowTea)

**定义**: 轻度发酵茶，具有"黄汤黄叶"特征。

**特征**:
- 发酵程度: 10%-20%
- 茶汤颜色: 杏黄明亮
- 口感: 醇和鲜爽
- 特殊工艺: 闷黄

**子类**:
- 黄芽茶 (YellowBudTea)
- 黄小茶 (YellowSmallTea)
- 黄大茶 (YellowLargeTea)

**著名品种**:
- 君山银针 (JunshanYinzhen)
- 蒙顶黄芽 (MengdingHuangya)
- 霍山黄芽 (HuanshanHuangya)

---

### 2.5 青茶/乌龙茶 (OolongTea)

**定义**: 半发酵茶，介于绿茶和红茶之间。

**特征**:
- 发酵程度: 15%-70%
- 茶汤颜色: 橙黄到红褐色
- 口感: 变化丰富
- 特殊工艺: 做青/摇青

**子类**:
- 闽北乌龙 (NorthernFujianOolong)
- 闽南乌龙 (SouthernFujianOolong)
- 广东乌龙 (GuangdongOolong)
- 台湾乌龙 (TaiwanOolong)

**著名品种**:
- 铁观音 (TieGuanYin)
- 大红袍 (DaHongPao)
- 冻顶乌龙 (DongDingOolong)
- 东方美人 (OrientalBeauty)
- 凤凰单丛 (PhoenixDancong)
- 肉桂 (Rougui)
- 水仙 (ShuiXian)

---

### 2.6 红茶 (BlackTea)

**定义**: 全发酵茶，茶汤红亮，滋味醇厚。

**特征**:
- 发酵程度: 100%
- 茶汤颜色: 红亮
- 口感: 醇厚甘甜
- 适合调饮

**子类**:
- 工夫红茶 (GongfuBlackTea)
- 红碎茶 (BrokenBlackTea)
- 小种红茶 (LapsangSouchong)

**著名品种**:
- 正山小种 (LapsangSouchong)
- 金骏眉 (Jinjunmei)
- 祁门红茶 (QimenBlackTea)
- 滇红 (YunnanBlackTea)
- 川红 (SichuanBlackTea)
- 宜兴红茶 (YixingBlackTea)
- 英德红茶 (YingdeBlackTea)
- 阿萨姆红茶 (Assam)
- 锡兰红茶 (Ceylon)
- 大吉岭红茶 (Darjeeling)

---

### 2.7 黑茶 (DarkTea)

**定义**: 后发酵茶，经过渥堆等特殊工艺。

**特征**:
- 发酵程度: 后发酵
- 茶汤颜色: 橙红到深红
- 口感: 醇滑回甘
- 储存特性: 越陈越醇

**子类**:
- 普洱茶 (Pu'erTea)
- 湖南黑茶 (HunanDarkTea)
- 湖北黑茶 (HubeiDarkTea)
- 四川边茶 (SichuanBorderTea)
- 广西六堡茶 (LiubaoTea)

**著名品种**:
- 普洱生茶 (RawPu'er)
- 普洱熟茶 (RipePu'er)
- 安化黑茶 (AnhuaDarkTea)
- 梧州六堡茶 (LiubaoTea)

---

### 2.8 再加工茶 (RefinedTea)

**定义**: 以基本茶类为原料进行再加工制成的茶。

**子类**:
- 花茶 (ScentedTea)
- 紧压茶 (CompressedTea)
- 萃取茶 (ExtractTea)
- 调味茶 (FlavoredTea)
- 保健茶 (HealthTea)

#### 2.8.1 花茶 (ScentedTea)

**定义**: 茶叶与鲜花窨制而成的茶。

**品种**:
- 茉莉花茶 (JasmineTea)
- 桂花茶 (OsmanthusTea)
- 玫瑰花茶 (RoseTea)
- 珠兰花茶 (ChrysanthemumTea)

#### 2.8.2 紧压茶 (CompressedTea)

**定义**: 蒸汽压制定型的茶。

**形态**:
- 砖茶 (BrickTea)
- 饼茶 (CakeTea)
- 沱茶 (TuoCha)
- 柱茶 (ColumnTea)

---

## 3. 茶树品种 (Tea Cultivar)

### 3.1 主要茶树品种

**中小叶种**:
- 龙井种 (LongjingCultivar)
- 碧螺春种 (BiluoCultivar)
- 铁观音种 (TieguanyinCultivar)
- 肉桂种 (RouguiCultivar)
- 水仙种 (ShuixianCultivar)

**大叶种**:
- 勐海大叶种 (MenghaiLargeLeaf)
- 凤庆大叶种 (FengqingLargeLeaf)
- 云南大叶种 (YunnanLargeLeaf)
- 阿萨姆种 (Assamica)

**性状**:
- `hasLeafSize`: 叶面积 (数值类型: cm²)
- `hasAromaType`: 香气类型 (枚举: 花香/果香/蜜香/木香)
- `hasResistance`: 抗性 (枚举: 抗寒/抗病/抗旱)
- `hasYield`: 产量 (数值类型: 公斤/亩)

---

## 4. 茶叶加工 (Tea Processing)

### 4.1 绿茶加工工艺

**工艺流程**:
- 杀青 (Fixation)
  - 炒青 (Pan-Firing)
  - 蒸青 (Steaming)
  - 烘青 (Baking)
- 揉捻 (Rolling)
- 干燥 (Drying)
  - 炒干 (Pan-Drying)
  - 烘干 (Oven-Drying)
  - 晒干 (Sun-Drying)

**参数**:
- 杀青温度: 180°C - 280°C
- 杀青时间: 2-10分钟
- 揉捻时间: 15-45分钟
- 干燥温度: 80°C - 120°C

---

### 4.2 红茶加工工艺

**工艺流程**:
- 萎凋 (Withering)
- 揉捻 (Rolling)
- 发酵 (Fermentation)
- 干燥 (Drying)

**参数**:
- 萎凋时间: 8-18小时
- 发酵温度: 20°C - 30°C
- 发酵时间: 2-6小时
- 干燥温度: 90°C - 120°C

---

### 4.3 乌龙茶加工工艺

**工艺流程**:
- 萎凋 (Withering)
- 做青/摇青 (Turning/Shaking)
- 杀青 (Fixation)
- 揉捻 (Rolling)
- 干燥 (Drying)

**特殊工艺**:
- 做青次数: 3-8次
- 摇青力度: 轻/中/重
- 发酵程度: 轻度/中度/重度

---

### 4.4 普洱茶加工工艺

**生普工艺**:
- 杀青 → 揉捻 → 晒干 → 蒸压 → 干燥

**熟普工艺**:
- 杀青 → 揉捻 → 晒干 → 渥堆 → 干燥 → 蒸压

**渥堆参数**:
- 渥堆温度: 40°C - 65°C
- 渥堆时间: 30-60天
- 洒水量: 25%-40%

---

## 5. 茶叶产区 (Tea Regions)

### 5.1 中国主要茶区

**江南茶区**:
- 浙江 (Zhejiang)
  - 西湖龙井产区
  - 安吉白茶产区
  - 越乡龙井产区
- 安徽 (Anhui)
  - 黄山毛峰产区
  - 祁门红茶产区
  - 六安瓜片产区
- 福建 (Fujian)
  - 闽北乌龙产区
  - 闽南乌龙产区
  - 白茶产区
- 江西 (Jiangxi)
  - 庐山云雾产区
  - 狗牯脑产区
- 湖南 (Hunan)
  - 君山银针产区
  - 安化黑茶产区
- 湖北 (Hubei)
  - 恩施玉露产区
  - 宜兴红茶产区

**华南茶区**:
- 广东 (Guangdong)
  - 凤凰单丛产区
  - 英德红茶产区
- 广西 (Guangxi)
  - 六堡茶产区
  - 桂花茶产区
- 福建 (Fujian)
  - 政和产区
  - 建阳产区
- 海南 (Hainan)
  - 五指山茶产区

**西南茶区**:
- 云南 (Yunnan)
  - 普洱茶产区
  - 滇红产区
  - 云南白茶产区
- 四川 (Sichuan)
  - 竹叶青产区
  - 蒙顶山茶产区
  - 川红产区
- 贵州 (Guizhou)
  - 都匀毛尖产区
  - 湄潭翠芽产区

**江北茶区**:
- 河南 (Henan)
  - 信阳毛尖产区
- 山东 (Shandong)
  - 崂山绿茶产区
- 陕西 (Shaanxi)
  - 紫阳富硒茶产区

---

### 5.2 国际茶区

**印度 (India)**:
- 阿萨姆 (Assam)
- 大吉岭 (Darjeeling)
- 尼尔吉里 (Nilgiri)

**斯里兰卡 (Sri Lanka)**:
- 锡兰高地茶
- 锡兰低地茶

**肯尼亚 (Kenya)**:
- 肯尼亚红茶

**日本 (Japan)**:
- 宇治茶 (Uji)
- 静冈茶 (Shizuoka)
- 狭山茶 (Sayama)

**韩国 (Korea)**:
- 宝城茶 (Boseong)
- 河东茶 (Hadong)

**越南 (Vietnam)**:
- 越南绿茶

---

## 6. 茶饮 (Tea Beverages)

### 6.1 原叶茶 (LeafTea)

**热泡**:
- 清饮 (PlainTea)
- 功夫茶 (GongfuCha)

**冷泡**:
- 冷萃茶 (ColdBrewTea)
- 冰滴茶 (IceDripTea)

---

### 6.2 调饮茶 (BlendedTea)

**奶茶系列**:
- 珍珠奶茶 (BubbleTea)
- 泰式奶茶 (ThaiMilkTea)
- 港式奶茶 (HongKongMilkTea)
- 蒙古奶茶 (MongolianMilkTea)

**果茶系列**:
- 水果茶 (FruitTea)
- 蜜桃乌龙 (PeachOolong)
- 柠檬红茶 (LemonBlackTea)

**创新茶饮**:
- 芝士茶 (CheeseTea)
- 奶盖茶 (MilkFoamTea)
- 气泡茶 (SparklingTea)

---

## 7. 茶具设备 (Tea Equipment)

### 7.1 泡茶器具 (BrewingWare)

**主泡器**:
- 紫砂壶 (YixingTeapot)
- 瓷壶 (PorcelainTeapot)
- 玻璃壶 (GlassTeapot)
- 盖碗 (GaiWan)
- 飘逸杯 (PiaoyiCup)

**辅助器具**:
- 茶海 (ChaHai)
- 公道杯 (GongdaoCup)
- 品茗杯 (TeaTastingCup)
- 闻香杯 (AromaCup)

**属性**:
- `hasMaterial`: 材质 (枚举: 紫砂/瓷/玻璃/金属/陶)
- `hasCapacity`: 容量 (毫升)
- `hasHeatRetention`: 保温性 (枚举: 优/良/一般)
- `hasPrice`: 价格 (货币类型)

---

### 7.2 储茶器具 (StorageWare)

**容器**:
- 茶叶罐 (TeaCaddy)
- 密封罐 (AirtightContainer)
- 冰箱冷藏 (RefrigeratedStorage)

**要求**:
- 遮光 (Light-Proof)
- 防潮 (Moisture-Proof)
- 防异味 (Odor-Proof)
- 密封 (Airtight)

---

### 7.3 辅助器具 (Accessories)

**器具**:
- 茶盘 (TeaTray)
- 茶巾 (TeaCloth)
- 茶夹 (TeaTongs)
- 茶匙 (TeaScoop)
- 茶针 (TeaNeedle)
- 茶漏 (TeaFilter)
- 电磁炉/电陶炉 (ElectricStove)
- 随手泡 (ElectricKettle)
- 温度计 (Thermometer)
- 电子秤 (Scale)

---

### 7.4 茶家具 (Tea Furniture)

- 茶桌 (TeaTable)
- 茶椅 (TeaChair)
- 博古架 (BookShelf)
- 茶车 (TeaCart)

---

## 8. 冲泡方法 (Brewing Methods)

### 8.1 功夫茶泡法 (GongfuCha)

**适用茶类**: 乌龙茶、红茶

**步骤**:
1. 温杯 (WarmCup)
2. 置茶 (AddTea)
3. 醒茶 (AwakenTea)
4. 冲泡 (Steep)
5. 出汤 (PourOut)
6. 分茶 (Serve)
7. 闻香 (Aroma)
8. 品茗 (Sip)

**参数**:
- 投茶量: 5-8克
- 水温: 85°C - 100°C
- 第一泡: 10-15秒
- 每一泡增加: 5-10秒
- 浸泡次数: 7-10次

---

### 8.2 盖碗泡法 (GaiWanBrewing)

**适用茶类**: 绿茶、白茶、黄茶

**参数**:
- 投茶量: 3-5克
- 水温: 75°C - 90°C
- 浸泡时间: 1-3分钟
- 出汤速度: 快速

---

### 8.3 紫砂壶泡法 (YixingPotBrewing)

**适用茶类**: 普洱茶、乌龙茶

**参数**:
- 投茶量: 壶容量的1/3到1/2
- 水温: 90°C - 100°C
- 浸泡时间: 10-30秒
- 温壶: 每次使用前热水温烫

---

### 8.4 玻璃杯泡法 (GlassBrewing)

**适用茶类**: 绿茶、花茶

**步骤**:
1. 烫杯 (WarmGlass)
2. 投茶 (AddTea)
3. 注水 (PourWater)
4. 观赏 (Observe)
5. 品饮 (Drink)

**参数**:
- 投茶量: 2-3克
- 水温: 75°C - 85°C
- 浸泡时间: 2-5分钟

---

### 8.5 冷泡法 (ColdBrewing)

**适用茶类**: 绿茶、白茶、红茶

**参数**:
- 投茶量: 5-10克
- 水温: 冷水/冰水
- 浸泡时间: 2-12小时
- 茶水比: 1:50 - 1:100

---

### 8.6 煮茶法 (BoilingTea)

**适用茶类**: 黑茶、老白茶

**参数**:
- 投茶量: 5-8克
- 水温: 煮沸
- 煮茶时间: 3-10分钟
- 煮沸次数: 3-5次

---

### 8.7 飘逸杯泡法 (PiaoyiCupBrewing)

**适用茶类**: 各类茶叶

**参数**:
- 投茶量: 3-5克
- 水温: 80°C - 100°C
- 浸泡时间: 30秒-3分钟
- 茶水分离: 自动分离

---

## 9. 感官评价 (Sensory Evaluation)

### 9.1 评茶指标

**外形 (Appearance)**:
- 条索 (Twist)
- 色泽 (Color)
- 整碎 (Uniformity)
- 净度 (Cleanliness)

**汤色 (Liquor Color)**:
- 亮度 (Brightness)
- 色调 (Hue)
- 清澈度 (Clarity)

**香气 (Aroma)**:
- 香型 (Aroma Type)
- 浓度 (Intensity)
- 持久度 (Persistence)
- 纯异度 (Purity)

**滋味 (Taste)**:
- 浓淡 (Strength)
- 甘甜 (Sweetness)
- 苦涩 (Bitterness)
- 醇厚 (Mouthfeel)
- 回甘 (Aftertaste)

**叶底 (Infused Leaf)**:
- 嫩度 (Tenderness)
- 色泽 (Color)
- 整碎 (Uniformity)

---

### 9.2 评分体系

**茶叶感官评分** (满分100分):

| 等级 | 分数 | 描述 |
|------|------|------|
| 特级 | 90-100 | 品质优异 |
| 一级 | 80-89 | 品质良好 |
| 二级 | 70-79 | 品质合格 |
| 三级 | 60-69 | 品质较差 |
| 不合格 | <60 | 不合格 |

---

### 9.3 风味描述

**花香类**:
- 茉莉花香 (Jasmine)
- 桂花香 (Osmanthus)
- 玫瑰花香 (Rose)
- 兰花香 (Orchid)
- 栀子花香 (Gardenia)

**果香类**:
- 蜜桃香 (Peach)
- 苹果香 (Apple)
- 柑橘香 (Citrus)
- 葡萄香 (Grape)
- 梅子香 (Plum)

**蜜香类**:
- 蜂蜜香 (Honey)
- 糖香 (Caramel)
- 麦芽香 (Malt)

**木香类**:
- 檀香 (Sandalwood)
- 沉香 (Agarwood)
- 松木香 (Pine)

**陈香类**:
- 仓储味 (Aged)
- 药香 (Herbal)
- 参香 (Ginseng)

---

## 10. 茶文化 (Tea Culture)

### 10.1 中国茶文化

**历史发展**:
- 神农时代: 茶叶发现
- 春秋战国: 茶叶饮用
- 唐代: 茶圣陆羽著《茶经》
- 宋代: 点茶文化
- 明代: 散茶冲泡
- 清代: 功夫茶形成

**茶道精神**:
- 和 (Harmony)
- 静 (Quietness)
- 清 (Pureness)
- 寂 (Simplicity)

**茶艺分类**:
- 绿茶茶艺
- 红茶茶艺
- 乌龙茶茶艺
- 普洱茶艺
- 花茶茶艺

---

### 10.2 各国茶文化

**日本茶道**:
- 茶道精神: 和敬清寂
- 茶道流派: 抹茶道/煎茶道
- 茶室: 茶室/露地
- 茶具: 茶碗/茶入/茶杓

**韩国茶礼**:
- 茶礼精神: 和敬俭美
- 茶礼类型: 传统茶礼/生活茶礼

**英国下午茶**:
- 时间: 15:00-17:00
- 传统: 三层点心架
- 茶种: 大吉岭、锡兰红茶

---

### 10.3 茶席 (Tea Setting)

**要素**:
- 茶叶 (Tea)
- 茶具 (Teaware)
- 茶水 (Water)
- 茶点 (TeaSnacks)
- 环境 (Environment)
- 礼仪 (Etiquette)

---

## 11. 茶叶产业链 (Tea Industry Chain)

### 11.1 种植环节 (Cultivation)

**参与者**:
- 茶农 (TeaFarmer)
- 茶叶合作社 (TeaCooperative)
- 茶园主 (TeaEstateOwner)

**活动**:
- 茶树栽培 (Cultivation)
- 茶园管理 (Management)
- 采摘 (Plucking)
- 病虫害防治 (PestControl)

---

### 11.2 加工环节 (Processing)

**参与者**:
- 初制所 (PrimaryProcessingFactory)
- 精制厂 (RefiningFactory)
- 茶叶加工企业 (TeaProcessingEnterprise)

**活动**:
- 鲜叶加工 (LeafProcessing)
- 精制加工 (Refining)
- 包装加工 (Packaging)

---

### 11.3 贸易环节 (Trade)

**参与者**:
- 茶叶经销商 (TeaDistributor)
- 茶叶批发商 (Wholesaler)
- 茶叶进出口商 (Importer/Exporter)
- 茶叶拍卖 (TeaAuction)

**交易模式**:
- 传统批发
- 电子商务
- 拍卖交易
- 期货交易

---

### 11.4 零售环节 (Retail)

**业态**:
- 茶叶专卖店 (TeaShop)
- 茶馆 (Teahouse)
- 连锁茶饮店 (TeaBeverageChain)
- 超市茶叶区 (Supermarket)
- 电商平台 (E-commerce)

---

## 12. 冲泡参数汇总 (Brewing Parameters Summary)

### 12.1 水温建议

| 茶类 | 建议水温 |
|------|----------|
| 绿茶 | 75°C - 85°C |
| 白茶 | 80°C - 90°C |
| 黄茶 | 80°C - 85°C |
| 乌龙茶 | 90°C - 100°C |
| 红茶 | 85°C - 95°C |
| 黑茶 | 95°C - 100°C |
| 花茶 | 85°C - 90°C |

---

### 12.2 投茶量建议

| 茶类 | 投茶量 | 容器容量 |
|------|--------|----------|
| 绿茶 | 3-5克 | 150ml |
| 白茶 | 5-8克 | 150ml |
| 乌龙茶 | 7-10克 | 110ml |
| 红茶 | 3-5克 | 150ml |
| 黑茶 | 8-10克 | 150ml |
| 花茶 | 3-5克 | 200ml |

---

### 12.3 浸泡时间

| 茶类 | 第一泡 | 第二泡 | 第三泡 |
|------|--------|--------|--------|
| 绿茶 | 1-2分钟 | 1-2分钟 | 1分钟 |
| 白茶 | 2-3分钟 | 3分钟 | 5分钟 |
| 乌龙茶 | 10-15秒 | 15-20秒 | 25-30秒 |
| 红茶 | 3-5分钟 | 5分钟 | 5分钟 |
| 黑茶 | 10-20秒 | 20-30秒 | 30-40秒 |

---

## 13. 关系图谱 (Relationship Graph)

```
TeaLeaf (茶叶)
  ├─ hasOrigin → TeaRegion (产区)
  ├─ hasCultivar → TeaCultivar (茶树品种)
  ├─ processedBy → TeaProcessing (加工工艺)
  ├─ hasType → TeaType (茶类)
  └─ belongsTo → TeaPlant (茶树)

TeaType (茶类)
  ├─ includes → GreenTea (绿茶)
  ├─ includes → WhiteTea (白茶)
  ├─ includes → YellowTea (黄茶)
  ├─ includes → OolongTea (乌龙茶)
  ├─ includes → BlackTea (红茶)
  └─ includes → DarkTea (黑茶)

TeaProcessing (加工工艺)
  ├─ includes → Fixation (杀青)
  ├─ includes → Rolling (揉捻)
  ├─ includes → Fermentation (发酵)
  ├─ includes → Drying (干燥)
  └─ produces → TeaProduct (茶制品)

TeaBeverage (茶饮)
  ├─ madeFrom → TeaLeaf (茶叶)
  ├─ brewedBy → BrewingMethod (冲泡方法)
  ├─ servedIn → TeaCup (茶具)
  └─ pairedWith → TeaSnacks (茶点)

BrewingMethod (冲泡方法)
  ├─ includes → GongfuCha (功夫茶)
  ├─ includes → GaiWan (盖碗)
  ├─ includes → ColdBrew (冷泡)
  └─ requires → Water (水)

TeaEquipment (茶具)
  ├─ includes → Teapot (茶壶)
  ├─ includes → GaiWan (盖碗)
  ├─ includes → TeaTray (茶盘)
  └─ madeOf → Material (材质)

TeaRegion (产区)
  ├─ locatedIn → China (中国茶区)
  ├─ locatedIn → India (印度)
  ├─ locatedIn → SriLanka (斯里兰卡)
  └─ produces → TeaCultivar (特色品种)
```

---

## 14. 本体复用 (Ontology Reuse)

**可复用的标准本体**:
- FOAF (人物组织)
- GeoNames (地理位置)
- Schema.org (通用概念)
- Dublin Core (元数据)

**命名空间映射**:
```xml
prefix tea: <http://tea-ontology.org/>
prefix foaf: <http://xmlns.com/foaf/0.1/>
prefix geo: <http://www.geonames.org/ontology#>
prefix schema: <https://schema.org/>
```

---

## 15. 版本历史

| 版本 | 日期 | 修改内容 |
|------|------|----------|
| 1.0.0 | 2026-03-16 | 初始版本 |

---

## 16. 参考资料

- 中国茶叶标准 (GB/T)
- 中国茶经
- 陆羽《茶经》
- SCA (Specialty Coffee Association) 感官评审标准
- 国际茶叶标准 (ISO)
- 各地方茶叶标准
