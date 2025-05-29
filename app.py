# %%
import streamlit as st
import pandas as pd
import numpy as np
import requests
import json

# 页面配置
st.set_page_config(
    page_title="Marketing Resource Hub",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 全局样式 */
    .main {
        padding: 2.5rem;
        background-color: #ffffff;
    }
    
    /* 导航菜单样式 */
    .css-1d391kg {
        background: linear-gradient(135deg, #1a237e 0%, #283593 70%, #3949ab 100%);
        padding: 2.5rem 1.5rem;
        box-shadow: 0 4px 20px rgba(26, 35, 126, 0.15);
    }
    
    .css-1d391kg .stRadio > label {
        color: #ffffff;
        font-size: 1.1rem;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1rem;
        cursor: pointer;
        background-color: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .css-1d391kg .stRadio > label:hover {
        background-color: rgba(255, 255, 255, 0.15);
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* 标题样式 */
    h1 {
        color: #1a237e;
        font-weight: 800;
        margin-bottom: 2rem;
        font-size: 2.75rem;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    
    h2 {
        color: #283593;
        font-weight: 700;
        margin-top: 2.5rem;
        font-size: 2rem;
        letter-spacing: -0.3px;
    }
    
    h3 {
        color: #3949ab;
        font-weight: 600;
        font-size: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
    
    /* 卡片样式 */
    .resource-card {
        background: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 1.8rem;
        border: 1px solid rgba(227, 233, 244, 0.8);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(26, 35, 126, 0.06);
        position: relative;
        overflow: hidden;
    }
    
    .resource-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .resource-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(26, 35, 126, 0.12);
        border-color: rgba(197, 202, 233, 0.8);
    }
    
    .resource-card:hover::before {
        opacity: 1;
    }
    
    .resource-card h4 {
        color: #1a237e;
        font-size: 1.4rem;
        margin-bottom: 1.2rem;
        font-weight: 600;
        letter-spacing: -0.2px;
    }
    
    .resource-card p {
        color: #5c6b89;
        line-height: 1.7;
        margin-bottom: 1.2rem;
        font-size: 1.05rem;
    }
    
    /* 按钮样式 */
    .view-button {
        display: inline-block;
        padding: 0.9rem 1.8rem;
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
        color: #ffffff !important;
        border-radius: 12px;
        text-decoration: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-top: 1.2rem;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(26, 35, 126, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
        font-size: 1.05rem;
    }
    
    .view-button:hover {
        background: linear-gradient(135deg, #283593 0%, #3949ab 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(26, 35, 126, 0.25);
    }
    
    /* 标签样式 */
    .tag {
        display: inline-block;
        padding: 0.5rem 1.3rem;
        border-radius: 25px;
        background-color: rgba(232, 234, 246, 0.8);
        color: #3949ab;
        margin-right: 1rem;
        margin-bottom: 1rem;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 500;
        border: 1px solid rgba(197, 202, 233, 0.3);
    }
    
    .tag:hover {
        background-color: rgba(197, 202, 233, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(26, 35, 126, 0.08);
    }
    
    /* 搜索框样式 */
    .stTextInput > div > div > input {
        border: 2px solid rgba(227, 233, 244, 0.8);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        font-size: 1.05rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(26, 35, 126, 0.04);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1a237e;
        box-shadow: 0 0 0 3px rgba(26, 35, 126, 0.1);
    }
    
    /* 分割线样式 */
    hr {
        margin: 2.5rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(to right, #1a237e, #3949ab);
        opacity: 0.15;
        border-radius: 2px;
    }
    
    /* 难度标签样式 */
    .difficulty {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-size: 0.95rem;
        font-weight: 500;
        margin-top: 0.8rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }
    
    .difficulty.beginner {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        color: #1976d2;
        border: 1px solid rgba(25, 118, 210, 0.1);
    }
    
    .difficulty.intermediate {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        color: #2e7d32;
        border: 1px solid rgba(46, 125, 50, 0.1);
    }
    
    .difficulty.advanced {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 100%);
        color: #c2185b;
        border: 1px solid rgba(194, 24, 91, 0.1);
    }
    
    /* 评分样式 */
    .rating {
        color: #1a237e;
        font-weight: 500;
        margin: 0.8rem 0;
        font-size: 1.05rem;
    }
    
    /* 链接样式 */
    a {
        color: #1a237e;
        text-decoration: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-bottom: 1px solid transparent;
    }
    
    a:hover {
        color: #3949ab;
        border-bottom-color: #3949ab;
    }
    
    /* 提示框样式 */
    .stAlert {
        background-color: rgba(232, 234, 246, 0.6);
        color: #1a237e;
        border-radius: 12px;
        border: 1px solid rgba(197, 202, 233, 0.4);
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 15px rgba(26, 35, 126, 0.06);
    }
    
    /* 页面头部样式 */
    .header-section {
        background: linear-gradient(135deg, #1a237e 0%, #283593 70%, #3949ab 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        color: white;
        box-shadow: 0 8px 30px rgba(26, 35, 126, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .header-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at top right, rgba(255,255,255,0.1) 0%, transparent 60%);
    }
    
    .header-section h2 {
        color: white;
        margin: 0;
        position: relative;
        font-size: 2.2rem;
    }
    
    .header-section p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.15rem;
        margin-top: 1.2rem;
        margin-bottom: 0;
        position: relative;
        line-height: 1.6;
    }
    
    /* 快速开始栏样式 */
    .quick-start {
        background: linear-gradient(135deg, #1a237e 0%, #283593 70%, #3949ab 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 16px;
        margin-top: 4rem;
        box-shadow: 0 8px 30px rgba(26, 35, 126, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .quick-start::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at top right, rgba(255,255,255,0.1) 0%, transparent 60%);
    }
    
    .quick-start h3 {
        color: white;
        margin-bottom: 1.8rem;
        position: relative;
    }
    
    .quick-start p {
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 1rem;
        position: relative;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    .quick-start .view-button {
        background: rgba(255, 255, 255, 0.12);
        margin-top: 1.8rem;
        backdrop-filter: blur(8px);
    }
    
    .quick-start .view-button:hover {
        background: rgba(255, 255, 255, 0.18);
    }
    
    /* 下拉框样式 */
    .stSelectbox > div > div {
        color: #333333 !important;
        background-color: white;
        border-radius: 12px;
        border: 2px solid rgba(227, 233, 244, 0.8);
        padding: 0.2rem;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #1a237e;
    }
    
    .stExpander {
        background-color: white;
        border: 1px solid rgba(227, 233, 244, 0.8);
        border-radius: 12px;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 15px rgba(26, 35, 126, 0.06);
    }
    
    .stExpander > div {
        color: #333333 !important;
        padding: 1.2rem;
    }
    
    .stExpander p {
        color: #5c6b89 !important;
        line-height: 1.7;
    }
    
    /* 关于页面容器样式 */
    .about-container {
        padding: 2.5rem;
        margin: 1.2rem 0;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(26, 35, 126, 0.06);
    }
    
    /* 个人头像样式 */
    .profile-image {
        margin-bottom: 2.5rem;
        position: relative;
    }
    
    .profile-image img {
        border-radius: 16px;
        box-shadow: 0 8px 30px rgba(26, 35, 126, 0.12);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .profile-image img:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(26, 35, 126, 0.18);
    }
    
    /* 滚动条美化 */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(227, 233, 244, 0.6);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(26, 35, 126, 0.2);
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(26, 35, 126, 0.3);
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    # 侧边栏导航
    with st.sidebar:
        st.title("🎯 导航菜单")
        st.markdown("---")
        navigation = {
            "🏠 首页": "首页",
            "📚 营销资料库": "营销资料库",
            "💼 求职招聘": "求职招聘",
            "📝 营销博客": "营销博客",
            "📊 数据分析学习": "数据分析学习",
            "🤖 AI助手": "AI助手",
            "👤 关于我": "关于我"
        }
        page = st.radio("", list(navigation.keys()))
        page = navigation[page]  # 获取对应的页面值

    if page == "首页":
        show_home_page()
    elif page == "营销资料库":
        show_marketing_resources()
    elif page == "求职招聘":
        show_job_resources()
    elif page == "营销博客":
        show_marketing_blogs()
    elif page == "数据分析学习":
        show_data_analytics()
    elif page == "AI助手":
        show_ai_assistant()
    elif page == "关于我":
        show_about()

def show_home_page():
    # 创建两列布局
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.title("营销资源整合平台")
        st.markdown("""
        <div style='background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.1);'>
            <h3>👋 欢迎来到您的一站式营销学习平台！</h3>
            <p style='font-size: 1.1rem; line-height: 1.6; color: #555;'>
            在这里，我们为营销专业的学生提供全方位的学习和发展资源。无论您是刚开始学习营销，还是正在寻找职业发展机会，
            我们都能为您提供有价值的帮助。
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 特色功能展示
        st.markdown("### ✨ 特色功能")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='resource-card'>
                <h4>📚 精选学习资源</h4>
                <p>海量营销理论与实践资料<br>行业案例分析<br>专业技能提升指南</p>
            </div>
            
            <div class='resource-card'>
                <h4>💼 求职发展</h4>
                <p>最新行业招聘信息<br>简历优化指导<br>求职经验分享</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class='resource-card'>
                <h4>📊 数据分析能力</h4>
                <p>营销数据分析教程<br>工具使用指南<br>实战项目演练</p>
            </div>
            
            <div class='resource-card'>
                <h4>🤖 AI助手</h4>
                <p>智能问答解惑<br>营销策略建议<br>案例分析辅助</p>
            </div>
            """, unsafe_allow_html=True)
    
    with right_col:
        # 用户引导卡片
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1a237e 0%, #283593 100%); color: white; padding: 2rem; border-radius: 10px; margin-top: 4rem;'>
            <h3 style='color: white; margin-bottom: 1.5rem;'>🎯 快速开始</h3>
            <p style='color: rgba(255, 255, 255, 0.9); margin-bottom: 0.8rem;'>1. 浏览营销资料库</p>
            <p style='color: rgba(255, 255, 255, 0.9); margin-bottom: 0.8rem;'>2. 探索求职机会</p>
            <p style='color: rgba(255, 255, 255, 0.9); margin-bottom: 0.8rem;'>3. 提升数据分析能力</p>
            <p style='color: rgba(255, 255, 255, 0.9); margin-bottom: 0.8rem;'>4. 与AI助手交流</p>
            <a href="#" class="view-button" style="background: rgba(255, 255, 255, 0.15); margin-top: 1.5rem; display: inline-block;">开始学习 →</a>
        </div>
        """, unsafe_allow_html=True)
        
        # 最新动态
        st.markdown("""
        <div class='resource-card' style='margin-top: 2rem;'>
            <h4>📢 最新动态</h4>
            <ul style='list-style-type: none; padding-left: 0;'>
                <li style='margin-bottom: 1rem;'>🆕 新增数字营销实战案例</li>
                <li style='margin-bottom: 1rem;'>📊 更新数据分析工具教程</li>
                <li style='margin-bottom: 1rem;'>💡 AI助手功能优化升级</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_marketing_resources():
    st.title("营销资料库")
    st.markdown("""
    <p style='font-size: 1.2rem; color: #666; margin-bottom: 2rem;'>
    探索丰富的营销学习资源，从理论到实践，助您成为出色的营销人才。
    </p>
    """, unsafe_allow_html=True)
    
    # 资料分类
    categories = {
        "营销理论基础": [
            {
                "title": "市场营销学原理",
                "link": "https://www.icourse163.org/course/XJTU-1206474807",
                "description": "西安交通大学精品课程，系统讲解营销基础理论",
                "tags": ["营销理论", "必修课程"],
                "difficulty": "入门级"
            },
            {
                "title": "数字营销专业证书",
                "link": "https://www.coursera.org/professional-certificates/google-digital-marketing-ecommerce",
                "description": "Google官方数字营销认证课程",
                "tags": ["数字营销", "专业认证"],
                "difficulty": "中级"
            },
            {
                "title": "腾讯广告大学",
                "link": "https://e.qq.com/ads/college/",
                "description": "腾讯官方营销学习平台，涵盖营销理论与实践",
                "tags": ["数字营销", "实战课程"],
                "difficulty": "入门到进阶"
            }
        ],
        "数字营销专题": [
            {
                "title": "巨量千川营销平台",
                "link": "https://qianchuan.jinritemai.com/",
                "description": "抖音官方营销平台，电商营销必备",
                "tags": ["短视频营销", "电商"],
                "difficulty": "中级"
            },
            {
                "title": "生意参谋",
                "link": "https://sycm.taobao.com/portal/home.htm",
                "description": "阿里巴巴官方商家数据分析平台",
                "tags": ["电商营销", "数据分析"],
                "difficulty": "进阶"
            },
            {
                "title": "微信视频号学习中心",
                "link": "https://channels.weixin.qq.com/platform/guide",
                "description": "微信官方视频号运营指南",
                "tags": ["内容营销", "短视频"],
                "difficulty": "入门"
            }
        ],
        "营销工具与平台": [
            {
                "title": "百度统计",
                "link": "https://tongji.baidu.com/web/welcome/login",
                "description": "免费专业的网站流量分析工具",
                "tags": ["数据分析", "用户洞察"],
                "difficulty": "中级"
            },
            {
                "title": "友盟+",
                "link": "https://www.umeng.com/",
                "description": "移动应用统计分析平台",
                "tags": ["数据分析", "用户研究"],
                "difficulty": "中级"
            },
            {
                "title": "微信广告投放平台",
                "link": "https://ad.weixin.qq.com/",
                "description": "微信生态广告投放与分析平台",
                "tags": ["广告投放", "效果分析"],
                "difficulty": "进阶"
            }
        ],
        "行业资源与报告": [
            {
                "title": "艾瑞咨询",
                "link": "https://www.iresearch.cn/",
                "description": "专业的互联网行业研究与咨询机构",
                "tags": ["行业报告", "数据研究"],
                "difficulty": "进阶"
            },
            {
                "title": "新榜",
                "link": "https://www.newrank.cn/",
                "description": "内容创作者数据分析平台",
                "tags": ["内容分析", "创作者经济"],
                "difficulty": "中级"
            },
            {
                "title": "卡思数据",
                "link": "https://www.caasdata.com/",
                "description": "专业的短视频数据分析平台",
                "tags": ["短视频分析", "数据洞察"],
                "difficulty": "进阶"
            }
        ],
        "实用学习资源": [
            {
                "title": "谷歌数字营销",
                "link": "https://skillshop.exceedlms.com/student/catalog/browse",
                "description": "Google官方数字营销课程平台",
                "tags": ["数字营销", "Google认证"],
                "difficulty": "中级"
            },
            {
                "title": "Facebook广告学习中心",
                "link": "https://www.facebook.com/business/learn",
                "description": "Meta官方营销学习资源",
                "tags": ["社交广告", "跨境营销"],
                "difficulty": "中级"
            },
            {
                "title": "LinkedIn营销解决方案",
                "link": "https://business.linkedin.com/marketing-solutions",
                "description": "LinkedIn官方营销学习平台",
                "tags": ["B2B营销", "职业营销"],
                "difficulty": "进阶"
            }
        ]
    }
    
    # 搜索和筛选功能
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 搜索资源", "")
    with col2:
        difficulty = st.selectbox("选择难度级别", ["全部", "入门级", "中级", "进阶", "高级"])
    
    for category, resources in categories.items():
        st.subheader(f"📚 {category}")
        
        # 筛选资源
        filtered_resources = resources
        if search:
            filtered_resources = [r for r in resources if search.lower() in r["title"].lower() or search.lower() in r["description"].lower()]
        if difficulty != "全部":
            filtered_resources = [r for r in filtered_resources if r["difficulty"] == difficulty]
        
        if not filtered_resources:
            st.info("没有找到符合条件的资源")
            continue
            
        cols = st.columns(3)
        for i, resource in enumerate(filtered_resources):
            with cols[i % 3]:
                st.markdown(f"""
                <div class='resource-card'>
                    <h4>{resource['title']}</h4>
                    <p style='color: #666;'>{resource['description']}</p>
                    <div style='margin: 1rem 0;'>
                        {' '.join([f"<span class='tag'>{tag}</span>" for tag in resource['tags']])}
                    </div>
                    <p style='color: #FF4B4B;'>难度: {resource['difficulty']}</p>
                    <a href="{resource['link']}" target="_blank" class="view-button">查看详情 →</a>
                </div>
                """, unsafe_allow_html=True)

def show_job_resources():
    st.title("求职招聘")
    st.write("---")
    
    # 求职网站推荐
    st.subheader("👔 求职网站导航")
    job_sites = {
        "综合招聘平台": [
            {"name": "LinkedIn", "url": "https://www.linkedin.com", "description": "全球最大的职业社交平台"},
            {"name": "智联招聘", "url": "https://www.zhaopin.com", "description": "国内领先的招聘网站"},
            {"name": "前程无忧", "url": "https://www.51job.com", "description": "覆盖面广的招聘平台"}
        ],
        "营销专业招聘": [
            {"name": "MarketingHire", "url": "https://www.marketinghire.com", "description": "营销专业人才招聘网站"},
            {"name": "MediaBistro", "url": "https://www.mediabistro.com", "description": "媒体营销职位发布平台"},
            {"name": "营销人网", "url": "https://www.marketers.com", "description": "营销行业垂直招聘平台"}
        ]
    }
    
    for category, sites in job_sites.items():
        st.write(f"#### {category}")
        for site in sites:
            st.markdown(f"""
            <div class="resource-card">
                <h4>{site['name']}</h4>
                <p>{site['description']}</p>
                <a href="{site['url']}" target="_blank" class="view-button">访问网站 →</a>
            </div>
            """, unsafe_allow_html=True)
    
    # 简历优化建议
    st.subheader("📝 简历优化建议")
    st.markdown("""
    1. 突出营销相关技能和经验
    2. 量化你的成就（ROI、增长率等）
    3. 展示数据分析能力
    4. 加入相关证书和培训经历
    5. 突出项目经验和实际成果
    """)

def show_marketing_blogs():
    st.title("营销博客")
    st.markdown("""
    <div class="header-section">
        <h2>精选优质营销资源</h2>
        <p>发现最新营销趋势、案例分析和专业内容</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 搜索框样式优化
    st.markdown("""
    <style>
    div[data-testid="stTextInput"] > div:first-child {
        background: white;
        padding: 0.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(26, 35, 126, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    search = st.text_input("🔍", placeholder="搜索博客、公众号或主题...")
    
    blogs = {
        "专业营销媒体": [
            {
                "name": "数英网",
                "url": "https://www.digitaling.com",
                "description": "国内领先的营销创意分享平台，提供最新营销案例和创意资讯",
                "topics": ["创意营销", "品牌案例", "行业资讯"],
                "rating": 4.8
            },
            {
                "name": "梅花网",
                "url": "https://www.meihua.info",
                "description": "专注于营销传播领域的专业网站，提供深度营销分析",
                "topics": ["营销传播", "案例分析", "行业趋势"],
                "rating": 4.7
            },
            {
                "name": "广告门",
                "url": "https://www.adquan.com",
                "description": "广告营销行业门户网站，提供最新营销动态",
                "topics": ["广告营销", "创意案例", "行业新闻"],
                "rating": 4.6
            }
        ],
        "优质营销公众号": [
            {
                "name": "品牌星球",
                "url": "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA5NDYxMTg2OQ==",
                "description": "专注品牌营销领域，分享品牌建设与营销策略",
                "topics": ["品牌营销", "策略分析", "案例解读"],
                "rating": 4.9
            },
            {
                "name": "营销之美",
                "url": "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA4NTk5MzE4OQ==",
                "description": "分享优秀营销案例和营销方法论",
                "topics": ["营销案例", "方法论", "实战技巧"],
                "rating": 4.8
            },
            {
                "name": "顶级营销案例",
                "url": "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI2MjE3OTA1MA==",
                "description": "深度解析优秀营销案例，提供实战指导",
                "topics": ["案例分析", "营销策略", "实战指南"],
                "rating": 4.7
            }
        ],
        "营销大咖博客": [
            {
                "name": "TopMarketing",
                "url": "https://www.topmarketing.cn",
                "description": "汇集营销大咖观点，分享前沿营销思想",
                "topics": ["营销思想", "行业观点", "趋势分析"],
                "rating": 4.8
            },
            {
                "name": "销售与市场",
                "url": "http://www.emkt.com.cn",
                "description": "专业的营销管理杂志官网，提供深度营销内容",
                "topics": ["营销管理", "市场策略", "案例研究"],
                "rating": 4.6
            }
        ],
        "短视频营销资讯": [
            {
                "name": "抖音营销研究院",
                "url": "https://school.jinritemai.com/doudian/web/article/101",
                "description": "抖音官方营销教程和最新资讯",
                "topics": ["短视频营销", "电商运营", "案例分享"],
                "rating": 4.9
            },
            {
                "name": "新榜营销观察",
                "url": "https://www.newrank.cn/public/info/list.html?period=day&type=data",
                "description": "新媒体营销数据分析和趋势报告",
                "topics": ["数据分析", "营销趋势", "内容策略"],
                "rating": 4.7
            }
        ]
    }
    
    for category, blog_list in blogs.items():
        st.subheader(f"📚 {category}")
        
        # 筛选博客
        filtered_blogs = blog_list
        if search:
            filtered_blogs = [
                b for b in blog_list 
                if search.lower() in b["name"].lower() 
                or search.lower() in b["description"].lower()
                or any(search.lower() in topic.lower() for topic in b["topics"])
            ]
            
        if not filtered_blogs:
            st.info("没有找到符合条件的资源")
            continue
            
        cols = st.columns(2)
        for idx, blog in enumerate(filtered_blogs):
            with cols[idx % 2]:
                st.markdown(f"""
                <div class="resource-card">
                    <h4>{blog['name']}</h4>
                    <p>{blog['description']}</p>
                    <div style='margin: 1rem 0;'>
                        {' '.join([f"<span class='tag'>{tag}</span>" for tag in blog['topics']])}
                    </div>
                    <p style='color: #FF4B4B;'>评分: {'⭐' * int(blog['rating'])}</p>
                    <a href="{blog['url']}" target="_blank" class="view-button">访问网站 →</a>
                </div>
                """, unsafe_allow_html=True)

def show_data_analytics():
    st.title("数据分析学习")
    st.markdown("""
    <div class="header-section">
        <h2>数据分析工具与技能</h2>
        <p>系统化的数据分析学习路径，助您掌握必备技能</p>
    </div>
    """, unsafe_allow_html=True)

    # 更新学习路径
    learning_paths = {
        "基础工具": [
            {
                "name": "Excel高级技能",
                "level": "入门",
                "importance": 90,
                "description": "数据分析的基础工具，包括数据处理、透视表和图表制作",
                "resources": [
                    "Microsoft Excel官方教程",
                    "LinkedIn Excel课程",
                    "Excel商业智能实战",
                    "VBA编程基础"
                ]
            },
            {
                "name": "SQL数据库",
                "level": "必备",
                "importance": 85,
                "description": "学习数据库查询和管理，处理大规模数据",
                "resources": [
                    "SQL基础教程",
                    "MySQL实战指南",
                    "PostgreSQL入门到精通",
                    "数据库设计最佳实践"
                ]
            },
            {
                "name": "Python基础",
                "level": "进阶",
                "importance": 80,
                "description": "使用Python进行数据分析和可视化",
                "resources": [
                    "Python入门课程",
                    "数据分析库教程",
                    "自动化数据处理",
                    "Python数据科学手册"
                ]
            }
        ],
        "数据可视化工具": [
            {
                "name": "Seaborn",
                "level": "进阶",
                "importance": 85,
                "description": "基于Matplotlib的统计数据可视化工具",
                "resources": [
                    "Seaborn官方文档",
                    "统计图表绘制",
                    "数据分布可视化",
                    "高级定制化教程"
                ]
            },
            {
                "name": "Matplotlib",
                "level": "必备",
                "importance": 90,
                "description": "Python最基础的绘图库",
                "resources": [
                    "Matplotlib基础教程",
                    "图形定制与美化",
                    "动态图表制作",
                    "科学绘图实战"
                ]
            },
            {
                "name": "Plotly",
                "level": "推荐",
                "importance": 80,
                "description": "交互式数据可视化库",
                "resources": [
                    "Plotly Express入门",
                    "交互式图表制作",
                    "数据仪表板开发",
                    "Web可视化集成"
                ]
            }
        ],
        "数据处理工具": [
            {
                "name": "Pandas",
                "level": "必备",
                "importance": 95,
                "description": "Python数据分析核心库",
                "resources": [
                    "Pandas基础教程",
                    "数据清洗与处理",
                    "高效数据操作",
                    "时间序列分析"
                ]
            },
            {
                "name": "Polars",
                "level": "进阶",
                "importance": 80,
                "description": "高性能数据处理库",
                "resources": [
                    "Polars入门指南",
                    "数据转换与聚合",
                    "性能优化技巧",
                    "大规模数据处理"
                ]
            }
        ],
        "机器学习工具": [
            {
                "name": "Scikit-learn",
                "level": "进阶",
                "importance": 90,
                "description": "机器学习算法库",
                "resources": [
                    "机器学习基础",
                    "模型训练与评估",
                    "特征工程",
                    "模型调优实战"
                ]
            },
            {
                "name": "TensorFlow",
                "level": "高级",
                "importance": 85,
                "description": "深度学习框架",
                "resources": [
                    "深度学习入门",
                    "神经网络构建",
                    "模型部署",
                    "GPU加速训练"
                ]
            },
            {
                "name": "PyTorch",
                "level": "高级",
                "importance": 85,
                "description": "动态深度学习框架",
                "resources": [
                    "PyTorch基础",
                    "深度学习模型",
                    "自定义网络层",
                    "分布式训练"
                ]
            }
        ],
        "AI开发工具": [
            {
                "name": "Bokeh",
                "level": "进阶",
                "importance": 75,
                "description": "交互式可视化应用开发",
                "resources": [
                    "Bokeh应用开发",
                    "交互式仪表板",
                    "实时数据可视化",
                    "Web应用部署"
                ]
            },
            {
                "name": "Streamlit",
                "level": "推荐",
                "importance": 85,
                "description": "数据应用快速开发框架",
                "resources": [
                    "Streamlit入门",
                    "数据应用构建",
                    "组件开发",
                    "应用部署"
                ]
            },
            {
                "name": "Gradio",
                "level": "推荐",
                "importance": 80,
                "description": "AI模型演示界面开发",
                "resources": [
                    "Gradio基础教程",
                    "模型接口开发",
                    "自定义界面",
                    "HuggingFace集成"
                ]
            }
        ]
    }

    # 选择学习路径
    path_selection = st.selectbox("选择学习路径", list(learning_paths.keys()))
    
    st.subheader(f"📊 {path_selection}")
    
    for skill in learning_paths[path_selection]:
        with st.expander(f"{skill['name']} ({skill['level']})"):
            st.markdown(f"""
            <div class='resource-card'>
                <p>{skill['description']}</p>
                <div style='margin: 1rem 0;'>
                    <div style='background-color: rgba(26, 35, 126, 0.1); height: 10px; border-radius: 5px;'>
                        <div style='background: linear-gradient(135deg, #1a237e 0%, #283593 100%); width: {skill['importance']}%; height: 100%; border-radius: 5px;'></div>
                    </div>
                    <p style='color: #333333; margin-top: 0.5rem;'>重要性: {skill['importance']}%</p>
                </div>
                <h4>学习资源：</h4>
                <ul style='color: #5c6b89;'>
                    {' '.join([f"<li>{resource}</li>" for resource in skill['resources']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)

def show_ai_assistant():
    st.title("AI营销助手")
    
    # 添加欢迎区域
    st.markdown("""
    <div class="header-section">
        <h2>👋 欢迎使用AI营销助手</h2>
        <p>您的智能营销顾问，随时为您提供专业的营销建议和解决方案</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 功能介绍
    st.markdown("""
    <div class='resource-card'>
        <h4>🎯 主要功能</h4>
        <ul style='color: #5c6b89; line-height: 1.8;'>
            <li>营销策略制定与优化建议</li>
            <li>市场调研与竞品分析指导</li>
            <li>营销文案与创意优化</li>
            <li>数据分析与洞察</li>
            <li>品牌定位与传播策略</li>
            <li>社交媒体营销建议</li>
        </ul>
    </div>
    
    <div class='resource-card'>
        <h4>💡 使用提示</h4>
        <ul style='color: #5c6b89; line-height: 1.8;'>
            <li>提供具体的背景信息，获得更精准的建议</li>
            <li>可以询问具体的营销案例分析</li>
            <li>支持多轮对话，逐步深入探讨</li>
            <li>欢迎随时提出跟进问题</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # 初始化会话状态
    init_session_state()
    
    # API配置
    api_key = "sk-ad5184cc837d4a6c9860bfa46ddd2c68"
    api_url = "https://api.deepseek.com/v1/chat/completions"
    
    # 配置请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        # 系统提示设置
        system_prompt = """你是一个专业的营销顾问，具备以下能力：
        1. 深入理解品牌营销策略
        2. 提供数据驱动的营销建议
        3. 分析行业趋势和竞品情况
        4. 优化营销传播策略
        5. 制定社交媒体营销方案
        6. 评估营销效果并提供改进建议
        
        请用专业、清晰且实用的方式回答问题，并尽可能提供具体的建议和可执行的方案。"""
        
        # 显示聊天界面
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 20px rgba(26, 35, 126, 0.06);'>
            <h3 style='color: #1a237e; margin-bottom: 1.5rem;'>💬 开始对话</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 显示聊天历史
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # 用户输入
        if prompt := st.chat_input("请输入您的营销相关问题..."):
            # 添加用户消息到界面
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # 准备API请求数据
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            messages.extend(st.session_state.messages)
            
            payload = {
                "model": "deepseek-chat",
                "messages": messages,
                "temperature": 0.7
            }
            
            # 调用API获取响应
            with st.spinner("思考中..."):
                try:
                    response = requests.post(api_url, headers=headers, json=payload)
                    
                    if response.status_code == 200:
                        response_data = response.json()
                        ai_response = response_data['choices'][0]['message']['content']
                        
                        # 添加AI响应到界面
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        with st.chat_message("assistant"):
                            st.markdown(ai_response)
                    else:
                        st.error(f"API调用失败: HTTP {response.status_code}")
                        st.code(response.text)  # 显示错误详情
                        
                except Exception as e:
                    st.error(f"获取AI响应时出错: {str(e)}")
                    
    except Exception as e:
        st.error(f"初始化AI助手时出错: {str(e)}")
        st.info("请确保API配置正确，并检查网络连接。")
    
    # 添加底部提示
    st.markdown("""
    <div style='margin-top: 2rem; padding: 1.5rem; background: rgba(232, 234, 246, 0.6); border-radius: 12px; border: 1px solid rgba(197, 202, 233, 0.4);'>
        <p style='color: #5c6b89; margin-bottom: 0;'>
            💡 <strong>小贴士：</strong> 如果您想获得更精准的建议，请提供具体的场景和需求。例如：
        </p>
        <ul style='color: #5c6b89; margin-top: 0.8rem;'>
            <li>如何提升我的社交媒体营销效果？</li>
            <li>请分析某品牌最近的营销活动优劣势</li>
            <li>如何制定新品上市的营销策略？</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def show_about():
    st.title("关于我")
    st.write("---")
    
    # 使用container来控制布局
    with st.container():
        # 增加页面边距和间距
        st.markdown("""
        <style>
        .about-container {
            padding: 2.5rem;
            margin: 1.2rem 0;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(26, 35, 126, 0.06);
        }
        .profile-image {
            margin-bottom: 2.5rem;
            position: relative;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # 创建两列，调整比例使布局更合理
        col1, col2 = st.columns([1, 2], gap="large")
        
        with col1:
            # 添加CSS类来控制图片样式
            st.markdown('<div class="profile-image">', unsafe_allow_html=True)
            st.image("生成吉卜力头像.png", width=250)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            ### 👋 个人简介
            
            我是姚晔昀，一名充满热情的市场营销专业学生。目前就读于香港中文大学商学院-市场营销（大数据营销方向），将于2025年7月入职FMCG市场部，期待在品牌营销与数字营销领域继续探索与成长。
            
            ### 🎯 专业方向
            * 数字营销策略
            * 数据驱动决策
            * 市场研究与分析
            * 渠道运营管理
            * 内容营销策划
            
            ### 💻 技术能力
            * 数据分析工具：Python、r、SPSS、AMOS、SQL，熟练运用Cursor, Trae等智能代码工具
            * 设计工具：PS、Canvas
            * 营销工具：各类数字营销平台

            ### 📱 联系方式
            * 📞 手机：(+86) 15000298072
            * 📧 邮箱：yaoyeyun0912@126.com
            """)

if __name__ == "__main__":
    main()

# %%
