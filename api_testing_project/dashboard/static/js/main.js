/**
 * Main JavaScript for API Testing Dashboard
 */

const runTestsBtn = document.getElementById('runTestsBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const progressSection = document.getElementById('progressSection');
const statusBadge = document.getElementById('statusBadge');
const toastContainer = document.getElementById('toastContainer');

const statTotal = document.getElementById('statTotal');
const statPassed = document.getElementById('statPassed');
const statFailed = document.getElementById('statFailed');
const statDuration = document.getElementById('statDuration');

const resultsContent = document.getElementById('resultsContent');
const categoriesSection = document.getElementById('categoriesSection');

let passFailChart = null;
let categoryChart = null;

document.addEventListener('DOMContentLoaded', () => {
    initializeCharts();
    loadResults();
    updateCategoryCards();
    setupEventListeners();
});

function setupEventListeners() {
    runTestsBtn.addEventListener('click', runTests);
}

async function runTests() {
    runTestsBtn.disabled = true;
    runTestsBtn.classList.add('loading');
    loadingSpinner.classList.add('active');
    progressSection.classList.add('active');
    updateStatusBadge('running', 'Running Tests');

    try {
        const response = await fetch('/run-tests', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to run tests');
        }

        const data = await response.json();
        await new Promise(resolve => setTimeout(resolve, 2000));
        await loadResults();
        document.getElementById('progressPercent').textContent = '100%';
        await new Promise(resolve => setTimeout(resolve, 500));

        showToast('success', '✓ Tests completed successfully!', 'All tests have been executed.');
        if (data.failed === 0) {
            updateStatusBadge('success', 'All Tests Passed');
        } else {
            updateStatusBadge('failed', `${data.failed} Tests Failed`);
        }

    } catch (error) {
        console.error('Error running tests:', error);
        showToast('error', '✗ Error running tests', error.message);
        updateStatusBadge('error', 'Test Execution Failed');
    } finally {
        runTestsBtn.disabled = false;
        runTestsBtn.classList.remove('loading');
        loadingSpinner.classList.remove('active');
        progressSection.classList.remove('active');
    }
}

async function loadResults() {
    try {
        const response = await fetch('/results');
        if (!response.ok) throw new Error('Failed to load results');
        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.error('Error loading results:', error);
    }
}

async function updateDashboard(data) {
    animateCounter(statTotal, parseInt(statTotal.textContent), data.total);
    animateCounter(statPassed, parseInt(statPassed.textContent), data.passed);
    animateCounter(statFailed, parseInt(statFailed.textContent), data.failed);
    displayTestResults(data);
    updatePassFailChart(data.passed, data.failed);
    updateCategoryChart(data.results_by_category);
    updateCategoryCards();
}

function animateCounter(element, start, end) {
    const duration = 1000;
    const steps = 30;
    const stepDuration = duration / steps;
    const increment = (end - start) / steps;

    let current = start;
    let step = 0;

    const counter = setInterval(() => {
        step++;
        current += increment;
        if (step >= steps) {
            current = end;
            clearInterval(counter);
        }
        element.textContent = Math.floor(current);
    }, stepDuration);
}

function displayTestResults(data) {
    if (!data.all_tests || data.all_tests.length === 0) {
        resultsContent.innerHTML = `
            <div class="empty-state">
                <div style="font-size: 3rem; margin-bottom: 1rem;"><i class="bi bi-inbox"></i></div>
                <p>No test results yet.</p>
            </div>
        `;
        return;
    }

    const table = document.createElement('table');
    table.className = 'results-table';
    table.innerHTML = `
        <thead>
            <tr>
                <th><i class="bi bi-hash"></i> Test Name</th>
                <th><i class="bi bi-tag"></i> Category</th>
                <th><i class="bi bi-check-circle"></i> Status</th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    `;

    const tbody = table.querySelector('tbody');

    data.all_tests.forEach((test, index) => {
        const row = document.createElement('tr');
        const isPass = test.includes('PASSED');
        const isFail = test.includes('FAILED');

        const category = getTestCategory(test);
        const statusBadge = isPass 
            ? '<span class="badge-pass"><i class="bi bi-check-circle"></i> PASS</span>'
            : '<span class="badge-fail"><i class="bi bi-x-circle"></i> FAIL</span>';

        const testName = extractTestName(test);

        row.innerHTML = `
            <td><code style="color: var(--text-secondary);">${testName}</code></td>
            <td><span class="badge-category">${category}</span></td>
            <td>${statusBadge}</td>
        `;

        tbody.appendChild(row);
    });

    resultsContent.innerHTML = '';
    resultsContent.appendChild(table);
}

function getTestCategory(testLine) {
    if (testLine.includes('test_unit') || testLine.includes('TestUnit')) return 'Unit';
    if (testLine.includes('test_functional') || testLine.includes('TestFunctional')) return 'Functional';
    if (testLine.includes('test_negative') || testLine.includes('TestNegative')) return 'Negative';
    if (testLine.includes('test_edge') || testLine.includes('TestEdge')) return 'Edge Case';
    if (testLine.includes('test_performance') || testLine.includes('TestPerformance')) return 'Performance';
    return 'Other';
}

function extractTestName(testLine) {
    const match = testLine.match(/test_\w+/i);
    return match ? match[0] : 'Unknown test';
}

function initializeCharts() {
    initPassFailChart();
    initCategoryChart();
}

function initPassFailChart() {
    const ctx = document.getElementById('passFailChart').getContext('2d');
    passFailChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Passed', 'Failed'],
            datasets: [{
                data: [0, 0],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(239, 68, 68, 0.8)'
                ],
                borderColor: [
                    'rgba(16, 185, 129, 1)',
                    'rgba(239, 68, 68, 1)'
                ],
                borderWidth: 2,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#cbd5e1',
                        font: { size: 12, weight: 600 },
                        padding: 15
                    }
                }
            }
        }
    });
}

function initCategoryChart() {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    categoryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Unit', 'Functional', 'Negative', 'Edge', 'Performance'],
            datasets: [{
                label: 'Tests Count',
                data: [0, 0, 0, 0, 0],
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(124, 58, 237, 0.8)'
                ],
                borderColor: [
                    'rgba(59, 130, 246, 1)',
                    'rgba(16, 185, 129, 1)',
                    'rgba(239, 68, 68, 1)',
                    'rgba(245, 158, 11, 1)',
                    'rgba(124, 58, 237, 1)'
                ],
                borderWidth: 2,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'x',
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(51, 65, 85, 0.2)' },
                    ticks: { color: '#cbd5e1' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#cbd5e1' }
                }
            }
        }
    });
}

function updatePassFailChart(passed, failed) {
    if (passFailChart) {
        passFailChart.data.datasets[0].data = [passed, failed];
        passFailChart.update();
    }
}

function updateCategoryChart(categories) {
    if (categoryChart && categories) {
        const data = [
            categories.unit?.total || 0,
            categories.functional?.total || 0,
            categories.negative?.total || 0,
            categories.edge?.total || 0,
            categories.performance?.total || 0
        ];
        categoryChart.data.datasets[0].data = data;
        categoryChart.update();
    }
}

async function updateCategoryCards() {
    try {
        const response = await fetch('/status');
        const data = await response.json();
        const counts = data.test_counts;

        const categories = [
            { name: 'Unit Tests', key: 'unit', icon: 'bi-microscope', color: '#3b82f6' },
            { name: 'Functional Tests', key: 'functional', icon: 'bi-check2-all', color: '#10b981' },
            { name: 'Negative Tests', key: 'negative', icon: 'bi-x-circle', color: '#ef4444' },
            { name: 'Edge Cases', key: 'edge', icon: 'bi-lightning', color: '#f59e0b' },
            { name: 'Performance Tests', key: 'performance', icon: 'bi-speedometer', color: '#7c3aed' }
        ];

        categoriesSection.innerHTML = categories
            .map((cat, i) => `
                <div class="category-card">
                    <div class="category-name">
                        <i class="bi ${cat.icon}" style="color: ${cat.color};"></i>
                        ${cat.name}
                    </div>
                    <div class="category-count">${counts[cat.key] || 0}</div>
                </div>
            `)
            .join('');

    } catch (error) {
        console.error('Error updating category cards:', error);
    }
}

function showToast(type, title, message) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const iconMap = {
        success: 'bi-check-circle',
        error: 'bi-x-circle',
        info: 'bi-info-circle'
    };

    toast.innerHTML = `
        <i class="bi ${iconMap[type]}"></i>
        <div>
            <strong>${title}</strong>
            <div style="font-size: 0.85rem;">${message}</div>
        </div>
    `;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 5000);
}

function updateStatusBadge(status, text) {
    const statusMap = {
        'idle': '#10b981',
        'running': '#3b82f6',
        'success': '#10b981',
        'failed': '#ef4444',
        'error': '#f59e0b'
    };

    const color = statusMap[status] || '#10b981';
    statusBadge.style.color = color;
    statusBadge.style.borderColor = color;
    statusBadge.innerHTML = `<i class="bi bi-circle-fill" style="font-size: 0.5rem;"></i> ${text}`;
}

setInterval(async () => {
    if (document.hidden) return;
    try {
        const response = await fetch('/results');
        const data = await response.json();
        if (data.status !== 'running') {
            updatePassFailChart(data.passed, data.failed);
        }
    } catch (error) {}
}, 5000);
