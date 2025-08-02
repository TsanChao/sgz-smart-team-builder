# 三国志战略版智能配将与协同分析工具 (sgz-smart-team-builder)

这个项目旨在为《三国志・战略版》玩家提供一个智能配将工具，通过分析武将和战法的协同效应，推荐最优的队伍搭配。

## 功能特点

1. **战法协同分析** - 分析不同战法之间的协同效应
2. **智能配将推荐** - 根据协同分析结果推荐最佳阵容
3. **数据管理** - 提供图形化界面维护武将和战法数据
4. **资源管理** - 管理和提供武将头像等静态资源

## 项目结构

```
sgz-smart-team-builder/
├── app.py                  # 后端主应用文件
├── config.py               # 配置文件
├── data/                   # 数据处理模块
│   ├── data_manager.py     # 数据管理器
│   └── consolidated_ocr_data.json  # 数据文件
├── core/                   # 核心逻辑模块
│   ├── synergy_analyzer.py # 战法协同分析器 (核心模块)
│   ├── recommender.py      # 推荐引擎
│   ├── level_calculator.py # 等级属性计算器
│   └── damage_calculator.py # 伤害计算器
├── api/                    # API接口模块
│   └── routes.py           # 路由定义
├── static/                 # 前端静态文件
│   ├── css/
│   ├── js/
│   └── index.html
└── assets/portraits/       # 武将头像图片
```

## 安装和运行

1. 克隆项目到本地
2. 安装依赖: `pip install -r requirements.txt`
3. 运行应用: `python app.py`
4. 在浏览器中访问: `http://localhost:5000`

## 更新机制

项目包含自动监控游戏公告更新的机制，可以及时获取游戏数据变更信息并更新本地数据。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。