# Mingye Glass 外贸独立站 - 项目文档

## 项目概述

Mingye Glass (明烨玻璃) 是一家专业玻璃制品外贸公司的独立站。
- **网站地址**: https://www.mingyeglass.net
- **域名**: www.mingyeglass.net (指向 GitHub Pages)
- **域名注册商**: 阿里云 (需要自行管理 DNS 解析)
- **部署方式**: GitHub Pages (已上线) / Vercel (已配置但未完整部署)

---

## 📁 文件结构

```
mingye-export/
├── website/                 # 网站完整源码（核心）
│   ├── index.html          # 首页
│   ├── products.html       # 产品分类页
│   ├── about.html          # 关于我们
│   ├── contact.html        # 联系我们
│   ├── 404.html            # 404页面
│   ├── CNAME               # 域名配置 (www.mingyeglass.net)
│   ├── vercel.json         # Vercel部署配置
│   ├── .github/workflows/  # GitHub Actions 自动部署配置
│   ├── css/style.css       # 样式文件
│   ├── js/main.js          # JavaScript
│   ├── images/             # 产品图片 (系列1~4)
│   ├── products/           # 系列产品详情页
│   │   ├── series1.html    # Beer Mugs & Drinkware
│   │   ├── series2.html    # Whiskey & Spirits
│   │   ├── series3.html    # Bakeware & Kitchen
│   │   └── series4.html    # Water Bottles & Cups
│   └── cn/                 # 中文版页面
├── admin.py                # Flask后台管理系统
├── fix_admin.py            # 后台系统修复脚本
├── README.md               # 本说明文档
└── credentials.txt         # 账号密码信息
```

---

## 🔧 工作流

### 1. 本地修改网站内容

**方式A - 直接编辑HTML文件（推荐快速修改）**
- 用 VS Code 或记事本打开 `website/` 下的 `.html` 文件
- 直接修改文字、图片链接等内容
- 保存后刷新浏览器即可看到效果

**方式B - 通过后台管理系统**
1. 运行后台服务器: `cd 项目目录 && python admin.py`
2. 浏览器访问: http://localhost:5000/admin
3. 登录密码: admin123
4. 在后台选择页面 → 编辑HTML → 保存

### 2. 本地预览网站

后台服务器运行后，访问以下地址：
- **网站前台**: http://localhost:5000/
- **后台管理**: http://localhost:5000/admin

### 3. 部署到线上

#### 方案A: GitHub Pages（推荐，已配置好）
1. 安装 Git (从 https://git-scm.com/ 下载)
2. 初始化仓库并推送到 GitHub:
   ```
   cd 项目目录/mingye-export/website
   git init
   git add .
   git commit -m "初始版本"
   git remote add origin https://github.com/songzhe849/mingyeglass-website.git
   git branch -M main
   git push -u origin main
   ```
3. 在 GitHub 仓库 → Settings → Pages → 选择 main 分支 → Save
4. 等待1-2分钟，网站就会在 https://songzhe849.github.io 上线
5. 域名 www.mingyeglass.net 已经通过CNAME指向了 GitHub Pages

#### 方案B: Vercel 部署
1. 登录 https://vercel.com (账号: mingyesong@hotmail.com)
2. 在 Vercel 后台创建一个 API Token
   - 打开 https://vercel.com/account/tokens
   - 点击 "Create" → 名称填 "My PC" → Full Scope → 创建
   - 复制生成的 Token
3. 将 Token 填入 GitHub 仓库 Secrets:
   - GitHub 仓库 → Settings → Secrets and variables → Actions
   - 添加 VERCEL_TOKEN、VERCEL_ORG_ID、VERCEL_PROJECT_ID
4. 推送代码到 main 分支自动部署

#### 方案C: 直接使用 Surge.sh（简单快速）
```
npm install -g surge
surge ./website mingye-glass.surge.sh
```

---

## 🔐 账号密码信息

详见同目录下的 `credentials.txt` 文件。

---

## 🌐 域名 DNS 配置

当前 www.mingyeglass.net 解析到 songzhe849.github.io (GitHub Pages IP)

如需修改，登录域名注册商（阿里云等）的 DNS 管理面板：
- CNAME 记录: www → songzhe849.github.io
- 如果使用 Vercel: CNAME 记录: www → cname.vercel-dns.com

---

## 🛠️ 后续开发建议

1. **产品页填充**: 系列2、3、4的产品页面目前是占位内容，需要从 images/系列2~4 中提取产品图片并填充HTML
2. **后台完善**: admin.py 可以进一步完善，增加更多的管理功能
3. **部署自动化**: 完善 GitHub Actions + Vercel 的自动化部署流程
4. **SEO优化**: 增加更多关键词和描述标签
5. **数据分析**: 接入 Google Analytics 等统计工具

---

*最后更新时间: 2026年6月30日*
