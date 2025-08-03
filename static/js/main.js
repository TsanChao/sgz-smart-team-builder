// 主JavaScript文件

// API基础URL
const API_BASE_URL = '/api';

document.addEventListener('DOMContentLoaded', function() {
    console.log('三国志战略版智能配将工具已加载');
    
    // 初始化应用
    initializeApp();
});

function initializeApp() {
    // 初始化武将选择界面
    initializeHeroSelection();
    
    // 初始化队伍推荐界面
    initializeTeamRecommendation();
    
    // 初始化协同分析界面
    initializeSynergyAnalysis();
    
    // 初始化公告界面
    initializeAnnouncementSection();
    
    // 加载元数据
    loadMetadata();
}

function loadMetadata() {
    fetch(`${API_BASE_URL}/metadata`)
        .then(response => response.json())
        .then(data => {
            window.metadata = data;
            console.log('元数据加载完成:', data);
        })
        .catch(error => {
            console.error('加载元数据失败:', error);
        });
}

function initializeHeroSelection() {
    console.log('初始化武将选择界面');
    loadHeroes();
}

function initializeTeamRecommendation() {
    console.log('初始化队伍推荐界面');
    setupRecommendationForm();
}

function initializeSynergyAnalysis() {
    console.log('初始化协同分析界面');
    setupSynergyForm();
}

function initializeAnnouncementSection() {
    console.log('初始化公告界面');
    loadAnnouncements();
}

function loadHeroes(page = 1, search = '') {
    const url = `${API_BASE_URL}/heroes?page=${page}&size=20&search=${encodeURIComponent(search)}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayHeroes(data.heroes, data.page, data.total_pages);
        })
        .catch(error => {
            console.error('加载武将数据失败:', error);
            document.getElementById('hero-selection').innerHTML = '<p>加载武将数据失败，请稍后重试。</p>';
        });
}

function displayHeroes(heroes, currentPage, totalPages) {
    const container = document.getElementById('hero-selection');
    let html = '<h2>武将选择</h2>';
    
    // 搜索框
    html += `
        <div class="search-box">
            <input type="text" id="hero-search" placeholder="搜索武将..." />
            <button onclick="searchHeroes()">搜索</button>
        </div>
    `;
    
    // 武将列表
    html += '<div class="hero-grid">';
    for (const [name, info] of Object.entries(heroes)) {
        html += `
            <div class="hero-card" onclick="selectHero('${name}')">
                <h3>${name}</h3>
                <p>阵营: ${info.阵营 || '未知'}</p>
                <p>武力: ${info.属性?.武力?.值 || '未知'}</p>
                <p>智力: ${info.属性?.智力?.值 || '未知'}</p>
                <p>统率: ${info.属性?.统率?.值 || '未知'}</p>
            </div>
        `;
    }
    html += '</div>';
    
    // 分页控件
    html += `
        <div class="pagination">
            <button onclick="loadHeroes(${Math.max(1, currentPage - 1)})" ${currentPage <= 1 ? 'disabled' : ''}>上一页</button>
            <span>第 ${currentPage} 页，共 ${totalPages} 页</span>
            <button onclick="loadHeroes(${Math.min(totalPages, currentPage + 1)})" ${currentPage >= totalPages ? 'disabled' : ''}>下一页</button>
        </div>
    `;
    
    container.innerHTML = html;
}

function searchHeroes() {
    const searchInput = document.getElementById('hero-search');
    const keyword = searchInput.value.trim();
    loadHeroes(1, keyword);
}

function selectHero(heroName) {
    // 添加武将到选中列表
    const selectedHeroes = window.selectedHeroes || [];
    if (!selectedHeroes.includes(heroName)) {
        selectedHeroes.push(heroName);
        window.selectedHeroes = selectedHeroes;
        updateSelectedHeroesDisplay();
    }
}

function updateSelectedHeroesDisplay() {
    const selectedHeroes = window.selectedHeroes || [];
    let html = '<h3>已选武将</h3><div class="selected-heroes">';
    for (const hero of selectedHeroes) {
        html += `<span class="selected-hero">${hero} <button onclick="removeSelectedHero('${hero}')">X</button></span>`;
    }
    html += '</div>';
    
    // 添加到武将选择界面
    const container = document.getElementById('hero-selection');
    container.innerHTML += html;
}

function removeSelectedHero(heroName) {
    const selectedHeroes = window.selectedHeroes || [];
    const index = selectedHeroes.indexOf(heroName);
    if (index > -1) {
        selectedHeroes.splice(index, 1);
        window.selectedHeroes = selectedHeroes;
        updateSelectedHeroesDisplay();
    }
}

function setupRecommendationForm() {
    const container = document.getElementById('team-recommendation');
    let html = `
        <h2>队伍推荐</h2>
        <form id="recommendation-form">
            <div>
                <label for="team-count">推荐队伍数量:</label>
                <input type="number" id="team-count" name="team-count" value="5" min="1" max="20">
            </div>
            <div>
                <label for="strategy">推荐策略:</label>
                <select id="strategy" name="strategy">
                    <option value="balanced">平衡型</option>
                    <option value="high_synergy">高协同</option>
                    <option value="diverse">多样化</option>
                </select>
            </div>
            <div>
                <label for="required-camp">必需阵营:</label>
                <select id="required-camp" name="required-camp">
                    <option value="">不限</option>
                </select>
            </div>
            <button type="button" onclick="getRecommendations()">获取推荐</button>
        </form>
        <div id="recommendation-results"></div>
    `;
    
    container.innerHTML = html;
    
    // 填充阵营选项
    if (window.metadata && window.metadata.camps) {
        const campSelect = document.getElementById('required-camp');
        window.metadata.camps.forEach(camp => {
            const option = document.createElement('option');
            option.value = camp;
            option.textContent = camp;
            campSelect.appendChild(option);
        });
    }
}

function getRecommendations() {
    const count = document.getElementById('team-count').value;
    const strategy = document.getElementById('strategy').value;
    const requiredCamp = document.getElementById('required-camp').value;
    const selectedHeroes = window.selectedHeroes || [];
    
    const requestData = {
        count: parseInt(count),
        strategy: strategy,
        required_camp: requiredCamp || undefined,
        required_hero: selectedHeroes.length > 0 ? selectedHeroes[0] : undefined  // 简化实现，只使用第一个选中的武将
    };
    
    fetch(`${API_BASE_URL}/recommend`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        displayRecommendations(data.teams);
    })
    .catch(error => {
        console.error('获取推荐失败:', error);
        document.getElementById('recommendation-results').innerHTML = '<p>获取推荐失败，请稍后重试。</p>';
    });
}

function displayRecommendations(teams) {
    const container = document.getElementById('recommendation-results');
    let html = '<h3>推荐队伍</h3>';
    
    if (teams.length === 0) {
        html += '<p>未找到符合条件的队伍推荐。</p>';
    } else {
        html += '<div class="team-list">';
        teams.forEach((team, index) => {
            html += `
                <div class="team-card">
                    <h4>推荐队伍 ${index + 1}</h4>
                    <ul>
                        ${team.heroes.map(hero => `<li>${hero}</li>`).join('')}
                    </ul>
                    <button onclick="analyzeTeamSynergy([${team.heroes.map(h => `'${h}'`).join(',')}])">分析协同</button>
                </div>
            `;
        });
        html += '</div>';
    }
    
    container.innerHTML = html;
}

function setupSynergyForm() {
    const container = document.getElementById('synergy-analysis');
    let html = `
        <h2>协同分析</h2>
        <div>
            <p>选择武将后点击"分析协同"按钮，或从推荐队伍中直接分析。</p>
            <button onclick="analyzeSelectedHeroesSynergy()">分析选中武将协同</button>
        </div>
        <div id="synergy-results"></div>
    `;
    
    container.innerHTML = html;
}

function analyzeSelectedHeroesSynergy() {
    const selectedHeroes = window.selectedHeroes || [];
    if (selectedHeroes.length === 0) {
        alert('请先选择武将');
        return;
    }
    
    analyzeTeamSynergy(selectedHeroes);
}

function analyzeTeamSynergy(heroes) {
    const requestData = {
        heroes: heroes,
        detailed: true
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
        displaySynergyAnalysis(data);
    })
    .catch(error => {
        console.error('分析协同失败:', error);
        document.getElementById('synergy-results').innerHTML = '<p>分析协同失败，请稍后重试。</p>';
    });
}

function displaySynergyAnalysis(data) {
    const container = document.getElementById('synergy-results');
    const analysis = data.synergy_analysis;
    
    let html = `
        <h3>协同分析结果</h3>
        <div class="synergy-score">
            <h4>协同评分: ${data.synergy_score}</h4>
        </div>
        <div class="synergy-details">
            <h4>详细分析</h4>
            <div class="analysis-section">
                <h5>标签分析</h5>
                <p>${analysis.标签分析?.分析 || '无数据'}</p>
            </div>
            <div class="analysis-section">
                <h5>兵种分析</h5>
                <p>${analysis.兵种分析?.分析 || '无数据'}</p>
            </div>
            <div class="analysis-section">
                <h5>阵营分析</h5>
                <p>${analysis.阵营分析?.加成说明 || '无数据'}</p>
            </div>
            <div class="analysis-section">
                <h5>战法分析</h5>
                <p>${analysis.战法分析?.协同潜力分析?.分析 || '无数据'}</p>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}

function loadAnnouncements(page = 1, search = '') {
    const url = `${API_BASE_URL}/announcements?page=${page}&size=10&search=${encodeURIComponent(search)}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayAnnouncements(data.announcements, data.page, data.total_pages);
        })
        .catch(error => {
            console.error('加载公告失败:', error);
            // 在适当的位置显示错误信息
        });
}

function displayAnnouncements(announcements, currentPage, totalPages) {
    // 实现公告展示逻辑
    console.log('显示公告:', announcements);
}