// 主JavaScript文件

// API基础URL
const API_BASE_URL = '/api';

// 确保在页面完全加载后初始化应用
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        console.log('DOMContentLoaded事件触发');
        initializeApp();
    });
} else {
    // 页面已经加载完成
    console.log('页面已加载完成，直接初始化应用');
    initializeApp();
}

window.addEventListener('load', function() {
    console.log('窗口加载事件触发');
});

function initializeApp() {
    console.log('开始初始化应用');
    
    // 设置导航标签事件
    setupNavigation();
    
    // 初始化智能配将模块
    initializeRecommendationModule();
    
    // 初始化数据管理模块
    initializeDataManagementModule();
    
    // 初始化关于模块
    initializeAboutModule();
    
    // 初始化模态框
    initializeModal();
    
    // 加载元数据
    loadMetadata();
    
    // 默认显示智能配将模块
    showModule('recommendation-module');
    
    console.log('应用初始化完成');
}

// 导航功能
function setupNavigation() {
    // 获取导航标签元素
    const recommendTab = document.getElementById('recommend-tab');
    const dataTab = document.getElementById('data-tab');
    const aboutTab = document.getElementById('about-tab');
    
    // 绑定点击事件
    if (recommendTab) {
        recommendTab.addEventListener('click', () => showModule('recommendation-module'));
    }
    
    if (dataTab) {
        dataTab.addEventListener('click', () => showModule('data-management-module'));
    }
    
    if (aboutTab) {
        aboutTab.addEventListener('click', () => showModule('about-module'));
    }
}

function showModule(moduleId) {
    // 隐藏所有模块
    document.querySelectorAll('.module').forEach(module => {
        module.classList.remove('active');
    });
    
    // 显示指定模块
    document.getElementById(moduleId).classList.add('active');
    
    // 更新导航标签状态
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // 根据模块ID设置活动标签
    if (moduleId === 'recommendation-module') {
        document.getElementById('recommend-tab').classList.add('active');
    } else if (moduleId === 'data-management-module') {
        document.getElementById('data-tab').classList.add('active');
    } else if (moduleId === 'about-module') {
        document.getElementById('about-tab').classList.add('active');
    }
}

function loadMetadata() {
    fetch(`${API_BASE_URL}/metadata`)
        .then(response => response.json())
        .then(data => {
            window.metadata = data;
            console.log('元数据加载完成:', data);
            // 填充下拉选择框
            populateSelectOptions();
        })
        .catch(error => {
            console.error('加载元数据失败:', error);
        });
}

function populateSelectOptions() {
    // 填充必须包含武将和排除武将的下拉框
    const requiredHeroSelect = document.getElementById('required-hero');
    const excludedHeroSelect = document.getElementById('excluded-hero');
    
    if (window.metadata && window.metadata.heroes) {
        // 清空现有选项
        requiredHeroSelect.innerHTML = '<option value="">请选择</option>';
        excludedHeroSelect.innerHTML = '<option value="">请选择</option>';
        
        // 添加武将选项
        window.metadata.heroes.forEach(hero => {
            const requiredOption = document.createElement('option');
            requiredOption.value = hero;
            requiredOption.textContent = hero;
            requiredHeroSelect.appendChild(requiredOption);
            
            const excludedOption = document.createElement('option');
            excludedOption.value = hero;
            excludedOption.textContent = hero;
            excludedHeroSelect.appendChild(excludedOption);
        });
    }
}

// 智能配将模块
function initializeRecommendationModule() {
    console.log('初始化智能配将模块');
    
    // 确保DOM元素存在后再绑定事件
    const startBtn = document.getElementById('start-recommendation');
    const resetBtn = document.getElementById('reset-settings');
    
    if (startBtn) {
        startBtn.addEventListener('click', getRecommendations);
        console.log('已绑定开始推荐按钮事件');
    } else {
        console.log('未找到开始推荐按钮');
    }
    
    if (resetBtn) {
        resetBtn.addEventListener('click', resetSettings);
        console.log('已绑定重置条件按钮事件');
    } else {
        console.log('未找到重置条件按钮');
    }
    
    console.log('智能配将模块初始化完成');
}

function resetSettings() {
    document.getElementById('required-hero').value = '';
    document.getElementById('excluded-hero').value = '';
    document.getElementById('recommend-level').value = '50';
    document.getElementById('recommend-count').value = '10';
    document.getElementById('troop-count').value = '10000';
    document.getElementById('damage-verification').checked = true;
}

function getRecommendations() {
    const requiredHero = document.getElementById('required-hero').value;
    const excludedHero = document.getElementById('excluded-hero').value;
    const level = document.getElementById('recommend-level').value;
    const count = document.getElementById('recommend-count').value;
    const troopCount = document.getElementById('troop-count').value;
    const damageVerification = document.getElementById('damage-verification').checked;
    
    const requestData = {
        数量: parseInt(count),
        等级: parseInt(level),
        兵力: parseInt(troopCount),
        伤害验证: damageVerification
    };
    
    if (requiredHero) {
        requestData.必须包含 = requiredHero;
    }
    
    if (excludedHero) {
        requestData.排除武将 = excludedHero;
    }
    
    fetch(`${API_BASE_URL}/recommend`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        // 修复：API返回的数据结构是 {count: 10, teams: [...]}
        // 需要传递 teams 数组给 displayRecommendations 函数
        if (data && data.teams) {
            displayRecommendations(data.teams);
        } else {
            displayRecommendations([]);
        }
    })
    .catch(error => {
        console.error('获取推荐失败:', error);
        document.getElementById('recommendation-list').innerHTML = '<p>获取推荐失败，请稍后重试。</p>';
    });
}

function displayRecommendations(teams) {
    const container = document.getElementById('recommendation-list');
    
    if (!teams || teams.length === 0) {
        container.innerHTML = '<p>未找到符合条件的队伍推荐。</p>';
        return;
    }
    
    let html = `<p>共找到 ${teams.length} 套阵容</p>`;
    html += '<div class="team-list">';
    
    teams.forEach((team, index) => {
        // 修复：API返回的数据结构是 {评分: 80.83, 队伍: ["马超", "张飞", "关兴"]}
        // 而不是 {协同评分: 80.83, 阵容: ["马超", "张飞", "关兴"]}
        html += `
            <div class="team-card">
                <h4>推荐阵容 ${index + 1}</h4>
                <p>协同评分: ${team.评分?.toFixed(1) || 'N/A'}</p>
                <p>阵容: ${team.队伍?.join(', ') || 'N/A'}</p>
                <button onclick="showSynergyDetails('${team.队伍?.join(',') || ''}')">查看详情</button>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

// 数据管理模块
function initializeDataManagementModule() {
    console.log('初始化数据管理模块');
    
    // 确保DOM元素存在后再绑定事件
    const addHeroBtn = document.getElementById('add-hero');
    const importBtn = document.getElementById('import-data');
    const exportBtn = document.getElementById('export-data');
    const refreshBtn = document.getElementById('refresh-data');
    const searchBtn = document.getElementById('search-data-button');
    
    if (addHeroBtn) {
        addHeroBtn.addEventListener('click', addHero);
        console.log('已绑定新增武将按钮事件');
    } else {
        console.log('未找到新增武将按钮');
    }
    
    if (importBtn) {
        importBtn.addEventListener('click', importData);
        console.log('已绑定导入数据按钮事件');
    } else {
        console.log('未找到导入数据按钮');
    }
    
    if (exportBtn) {
        exportBtn.addEventListener('click', exportData);
        console.log('已绑定导出数据按钮事件');
    } else {
        console.log('未找到导出数据按钮');
    }
    
    if (refreshBtn) {
        refreshBtn.addEventListener('click', refreshData);
        console.log('已绑定刷新按钮事件');
    } else {
        console.log('未找到刷新按钮');
    }
    
    if (searchBtn) {
        searchBtn.addEventListener('click', searchData);
        console.log('已绑定搜索按钮事件');
    } else {
        console.log('未找到搜索按钮');
    }
    
    // 初始化数据表格
    loadHeroData(1);
    
    // 初始化战法数据表格
    loadSkillData(1);
}

function loadHeroData(page = 1, search = '', camp = '') {
    // 构建API URL，包含分页、搜索和阵营筛选参数
    let url = `${API_BASE_URL}/heroes?page=${page}&size=20`;
    if (search) {
        url += `&search=${encodeURIComponent(search)}`;
    }
    if (camp) {
        url += `&camp=${encodeURIComponent(camp)}`;
    }
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayHeroData(data);
        })
        .catch(error => {
            console.error('加载武将数据失败:', error);
            document.getElementById('hero-data-table').innerHTML = '<p>加载武将数据失败，请稍后重试。</p>';
        });
}

function loadSkillData(page = 1, search = '', skillType = '') {
    // 构建API URL，包含分页、搜索和类型筛选参数
    let url = `${API_BASE_URL}/skills?page=${page}&size=20`;
    if (search) {
        url += `&search=${encodeURIComponent(search)}`;
    }
    if (skillType) {
        url += `&type=${encodeURIComponent(skillType)}`;
    }
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            displaySkillData(data);
        })
        .catch(error => {
            console.error('加载战法数据失败:', error);
            document.getElementById('skill-data-table').innerHTML = '<p>加载战法数据失败，请稍后重试。</p>';
        });
}

function displayHeroData(heroes) {
    const container = document.getElementById('hero-data-table');
    
    if (!heroes || !heroes.heroes) {
        container.innerHTML = '<p>暂无武将数据。</p>';
        return;
    }
    
    // 获取分页信息
    const page = heroes.page || 1;
    const size = heroes.size || 20;
    const totalPages = heroes.total_pages || 1;
    const count = heroes.count || Object.keys(heroes.heroes).length;
    
    let html = `
        <div class="table-info">
            <p>共 ${count} 名武将，第 ${page} 页，共 ${totalPages} 页</p>
        </div>
        <table class="data-table">
            <thead>
                <tr>
                    <th>姓名</th>
                    <th>阵营</th>
                    <th>统御</th>
                    <th>标签</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    // 显示武将数据
    Object.entries(heroes.heroes).forEach(([name, info]) => {
        html += `
            <tr>
                <td>${name}</td>
                <td>${info.阵营 || '未知'}</td>
                <td>${info.统御 || '未知'}</td>
                <td>${(info.标签 || []).join(', ')}</td>
                <td>
                    <button onclick="editHero('${name}')">编辑</button>
                </td>
            </tr>
        `;
    });
    
    html += `
            </tbody>
        </table>
        <div class="pagination">
            <button onclick="loadHeroData(${Math.max(1, page - 1)})" ${page <= 1 ? 'disabled' : ''}>上一页</button>
            <span>第 ${page} 页，共 ${totalPages} 页</span>
            <button onclick="loadHeroData(${Math.min(totalPages, page + 1)})" ${page >= totalPages ? 'disabled' : ''}>下一页</button>
        </div>
    `;
    
    container.innerHTML = html;
}

function displaySkillData(skills) {
    const container = document.getElementById('skill-data-table');
    
    if (!skills || !skills.skills) {
        container.innerHTML = '<p>暂无战法数据。</p>';
        return;
    }
    
    // 获取分页信息
    const page = skills.page || 1;
    const size = skills.size || 20;
    const totalPages = skills.total_pages || 1;
    const count = skills.count || Object.keys(skills.skills).length;
    
    let html = `
        <div class="table-info">
            <p>共 ${count} 个战法，第 ${page} 页，共 ${totalPages} 页</p>
        </div>
        <table class="data-table">
            <thead>
                <tr>
                    <th>名称</th>
                    <th>类型</th>
                    <th>品质</th>
                    <th>发动概率</th>
                    <th>描述</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
    `;
    
    // 显示战法数据
    Object.entries(skills.skills).forEach(([name, info]) => {
        // 转义单引号以避免JavaScript语法错误
        const escapedName = name.replace(/'/g, "\\'");
        const infoStr = JSON.stringify(info).replace(/'/g, "\\'");
        html += `
            <tr>
                <td>${name}</td>
                <td>${info.类型 || '未知'}</td>
                <td>${info.品质 || '未知'}</td>
                <td>${info.发动概率 || '未知'}</td>
                <td>${info.描述 || '无描述'}</td>
                <td>
                    <button onclick="editSkill('${escapedName}', ${infoStr})">编辑</button>
                </td>
            </tr>
        `;
    });
    
    html += `
            </tbody>
        </table>
        <div class="pagination">
            <button onclick="loadSkillData(${Math.max(1, page - 1)})" ${page <= 1 ? 'disabled' : ''}>上一页</button>
            <span>第 ${page} 页，共 ${totalPages} 页</span>
            <button onclick="loadSkillData(${Math.min(totalPages, page + 1)})" ${page >= totalPages ? 'disabled' : ''}>下一页</button>
        </div>
    `;
    
    container.innerHTML = html;
}

function addHero() {
    alert('新增武将功能待实现');
}

function importData() {
    alert('导入数据功能待实现');
}

function exportData() {
    alert('导出数据功能待实现');
}

function refreshData() {
    // 刷新时从第一页开始，不清空搜索词和筛选条件
    const keyword = document.getElementById('data-search').value.trim();
    const camp = document.getElementById('hero-camp-filter') ? document.getElementById('hero-camp-filter').value : '';
    const skillType = document.getElementById('skill-type-filter') ? document.getElementById('skill-type-filter').value : '';
    loadHeroData(1, keyword, camp);
    loadSkillData(1, keyword, skillType);
}

function searchData() {
    const keyword = document.getElementById('data-search').value.trim();
    const camp = document.getElementById('hero-camp-filter') ? document.getElementById('hero-camp-filter').value : '';
    const skillType = document.getElementById('skill-type-filter') ? document.getElementById('skill-type-filter').value : '';
    // 搜索时从第一页开始
    loadHeroData(1, keyword, camp);
    loadSkillData(1, keyword, skillType);
}

function filterHeroData() {
    const camp = document.getElementById('hero-camp-filter').value;
    const keyword = document.getElementById('data-search').value.trim();
    // 筛选时从第一页开始
    loadHeroData(1, keyword, camp);
}

function filterSkillData() {
    const skillType = document.getElementById('skill-type-filter').value;
    const keyword = document.getElementById('data-search').value.trim();
    // 筛选时从第一页开始
    loadSkillData(1, keyword, skillType);
}

function editHero(heroName) {
    alert(`编辑武将 ${heroName} 功能待实现`);
}

function deleteHero(heroName) {
    if (confirm(`确定要删除武将 ${heroName} 吗？`)) {
        alert(`删除武将 ${heroName} 功能待实现`);
    }
}

// 关于模块
function initializeAboutModule() {
    // 关于模块内容已在HTML中定义，此处无需额外处理
}

// 模态框功能
function initializeModal() {
    const modal = document.getElementById('synergy-modal');
    const closeBtn = document.querySelector('.modal .close');
    
    if (modal && closeBtn) {
        // 点击关闭按钮关闭模态框
        closeBtn.onclick = function() {
            modal.style.display = 'none';
        };
        
        // 点击模态框外部关闭模态框
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        };
    }
    
    // 初始化战法编辑模态框
    initializeSkillEditModal();
}

function initializeSkillEditModal() {
    const modal = document.getElementById('skill-edit-modal');
    const closeBtn = modal.querySelector('.close');
    const cancelBtn = document.getElementById('cancel-skill-edit');
    const form = document.getElementById('skill-edit-form');
    
    // 点击关闭按钮关闭模态框
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    };
    
    // 点击取消按钮关闭模态框
    cancelBtn.onclick = function() {
        modal.style.display = 'none';
    };
    
    // 点击模态框外部关闭模态框
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };
    
    // 处理表单提交
    form.onsubmit = function(e) {
        e.preventDefault();
        saveSkill();
    };
}

function editSkill(skillName, skillInfo) {
    // 填充表单数据
    document.getElementById('skill-original-name').value = skillName;
    document.getElementById('skill-name').value = skillName;
    document.getElementById('skill-type').value = skillInfo.类型 || '主动';
    document.getElementById('skill-quality').value = skillInfo.品质 || 'S';
    document.getElementById('skill-probability').value = skillInfo.发动概率 || '';
    document.getElementById('skill-description').value = skillInfo.描述 || '';
    
    // 显示模态框
    document.getElementById('skill-edit-modal').style.display = 'block';
}

function saveSkill() {
    // 获取表单数据
    const originalName = document.getElementById('skill-original-name').value;
    const name = document.getElementById('skill-name').value;
    const type = document.getElementById('skill-type').value;
    const quality = document.getElementById('skill-quality').value;
    const probability = document.getElementById('skill-probability').value;
    const description = document.getElementById('skill-description').value;
    
    // 构造战法信息对象
    const skillInfo = {
        类型: type,
        品质: quality,
        发动概率: probability,
        描述: description
    };
    
    // 发送更新请求
    fetch(`${API_BASE_URL}/skills/${encodeURIComponent(originalName)}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(skillInfo)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            // 关闭模态框
            document.getElementById('skill-edit-modal').style.display = 'none';
            // 刷新战法数据
            refreshData();
        } else {
            alert('更新战法失败: ' + (data.error || '未知错误'));
        }
    })
    .catch(error => {
        console.error('更新战法失败:', error);
        alert('更新战法失败，请稍后重试。');
    });
}

function showSynergyDetails(heroesString) {
    const heroes = heroesString.split(',');
    
    // 构造请求数据
    const requestData = {
        阵容: heroes,
        等级: parseInt(document.getElementById('recommend-level').value) || 50
    };
    
    fetch(`${API_BASE_URL}/synergy`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        displaySynergyDetails(data, heroes);
        document.getElementById('synergy-modal').style.display = 'block';
    })
    .catch(error => {
        console.error('获取协同分析详情失败:', error);
        alert('获取协同分析详情失败，请稍后重试。');
    });
}

function displaySynergyDetails(data, heroes) {
    const container = document.getElementById('synergy-details');
    
    let html = `
        <h2>协同分析 - ${heroes.join(',')}</h2>
        <div class="synergy-score">
            <h3>队伍协同评分: ${data.synergy_score?.toFixed(1) || 'N/A'}</h3>
        </div>
    `;
    
    // 战法协同效应
    if (data.synergy_analysis?.战法分析?.协同潜力分析?.分析) {
        html += `
            <div class="analysis-section">
                <h4>战法协同效应</h4>
                <p>${data.synergy_analysis.战法分析.协同潜力分析.分析}</p>
            </div>
        `;
    }
    
    // 队伍角色搭配
    if (data.synergy_analysis?.角色分析) {
        html += `
            <div class="analysis-section">
                <h4>队伍角色搭配</h4>
                <p>${JSON.stringify(data.synergy_analysis.角色分析)}</p>
            </div>
        `;
    }
    
    // 改进建议
    html += `
        <div class="analysis-section">
            <h4>改进建议</h4>
            <p>根据协同分析结果，可以考虑调整阵容搭配以提高整体协同效果。</p>
        </div>
    `;
    
    container.innerHTML = html;
}

// 分页函数
function goToPage(page) {
    const keyword = document.getElementById('data-search').value.trim();
    loadHeroData(page, keyword);
}

function goToSkillPage(page) {
    const keyword = document.getElementById('data-search').value.trim();
    loadSkillData(page, keyword);
}

function searchHeroes() {
    // 此函数用于智能配将模块的搜索功能
    console.log('搜索功能待实现');
}

// 切换数据标签页
function switchDataTab(tab) {
    // 隐藏所有数据表格
    document.getElementById('hero-data-table').style.display = 'none';
    document.getElementById('skill-data-table').style.display = 'none';
    
    // 隐藏所有筛选控件
    document.getElementById('hero-filter-box').style.display = 'none';
    document.getElementById('skill-filter-box').style.display = 'none';
    
    // 移除所有标签的活动状态
    document.querySelectorAll('.data-tab').forEach(t => t.classList.remove('active'));
    
    // 显示选中的表格和筛选控件并设置活动状态
    if (tab === 'hero') {
        document.getElementById('hero-data-table').style.display = 'block';
        document.getElementById('hero-filter-box').style.display = 'block';
        document.querySelector('.data-tab[data-tab="hero"]').classList.add('active');
    } else if (tab === 'skill') {
        document.getElementById('skill-data-table').style.display = 'block';
        document.getElementById('skill-filter-box').style.display = 'block';
        document.querySelector('.data-tab[data-tab="skill"]').classList.add('active');
    }
}