const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const clearBtn = document.getElementById('search-clear');
const dictContent = document.querySelector('.dict-content');
const headerTitle = document.querySelector('.dict-header-title');
const headerCount = document.querySelector('.dict-header-count');
const tabs = document.querySelectorAll('.dict-tab');

let currentDict = 'jako';

const DICT_LABELS = {
    jako: '일한사전',
    hanja: '한자사전',
};

// 클리어 버튼 표시/숨기기
function updateClearBtn() {
    clearBtn.classList.toggle('visible', searchInput.value.length > 0);
}

searchInput.addEventListener('input', updateClearBtn);

clearBtn.addEventListener('click', () => {
    searchInput.value = '';
    updateClearBtn();
    searchInput.focus();
});

// 탭 전환
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentDict = tab.dataset.dict;
        headerTitle.textContent = DICT_LABELS[currentDict];
        headerCount.textContent = '';

        if (searchInput.value.trim()) {
            doSearch();
        }
    });
});

// 검색 실행
function doSearch() {
    const query = searchInput.value.trim();
    if (!query) {
        showStatus('📖', '검색어를 입력하세요');
        return;
    }

    showLoading();

    fetch(`/api/search?q=${encodeURIComponent(query)}&dict=${currentDict}&limit=30`)
        .then(res => {
            if (!res.ok) throw new Error('서버 오류');
            return res.json();
        })
        .then(data => {
            if (data.count === 0) {
                showStatus('🔍', `"${query}"에 대한 결과가 없습니다`);
                headerCount.textContent = '';
                return;
            }

            headerCount.textContent = `${data.count}건`;

            const html = data.results.map(r =>
                `<h3>${escapeHtml(r.word)}</h3>${r.definition}`
            ).join('<br><br>');

            dictContent.innerHTML = html;
            dictContent.scrollTop = 0;
        })
        .catch(err => {
            console.error(err);
            showStatus('⚠️', '검색 중 오류가 발생했습니다');
        });
}

function showLoading() {
    dictContent.innerHTML = `
        <div class="status-message">
            <div class="spinner"></div>
            <span class="status-text">검색 중...</span>
        </div>`;
    headerCount.textContent = '';
}

function showStatus(icon, text) {
    dictContent.innerHTML = `
        <div class="status-message">
            <span class="status-icon">${icon}</span>
            <span class="status-text">${text}</span>
        </div>`;
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// 이벤트 바인딩
searchBtn.addEventListener('click', doSearch);
searchInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') doSearch();
});

// 닫기 버튼 — 결과 초기화
document.querySelector('.dict-close').addEventListener('click', () => {
    searchInput.value = '';
    updateClearBtn();
    headerCount.textContent = '';
    showStatus('📖', '검색어를 입력하세요');
});

// 페이지 로드 시 입력창 포커스
searchInput.focus();
