/**
 * Charts for SEO Analyzer
 * This file contains the chart configurations for visualizing SEO data
 */

// Common chart configuration options
const commonChartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
        legend: {
            position: 'top',
        }
    }
};

/**
 * Creates a gauge chart for performance scores
 * @param {string} canvasId - The canvas element ID
 * @param {number} score - The score value (0-100)
 * @param {string} label - The label for the chart
 */
function createGaugeChart(canvasId, score, label) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    // Get chart color based on score
    let color;
    if (score >= 90) {
        color = 'rgba(40, 167, 69, 0.8)'; // green
    } else if (score >= 50) {
        color = 'rgba(255, 193, 7, 0.8)';  // yellow
    } else {
        color = 'rgba(220, 53, 69, 0.8)';  // red
    }
    
    const ctx = canvas.getContext('2d');
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: [
                    color,
                    'rgba(0, 0, 0, 0.1)'
                ],
                borderWidth: 0
            }]
        },
        options: {
            cutout: '80%',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    });
}

/**
 * Creates a bar chart for score comparisons
 * @param {string} canvasId - The canvas element ID
 * @param {Array} labels - The labels for each bar
 * @param {Array} yourScores - Your website's scores
 * @param {Array} competitorScores - Competitor's scores
 */
function createComparisonChart(canvasId, labels, yourScores, competitorScores) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Your Website',
                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1,
                    data: yourScores
                },
                {
                    label: 'Competitor',
                    backgroundColor: 'rgba(255, 99, 132, 0.7)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    data: competitorScores
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Score'
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Performance Metrics Comparison'
                }
            }
        }
    });
}

/**
 * Creates a radar chart for keyword density comparison
 * @param {string} canvasId - The canvas element ID
 * @param {Array} keywords - The keywords to compare
 * @param {Array} yourDensity - Your website's keyword density values
 * @param {Array} competitorDensity - Competitor's keyword density values
 */
function createKeywordRadarChart(canvasId, keywords, yourDensity, competitorDensity) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: keywords,
            datasets: [
                {
                    label: 'Your Website',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    pointBackgroundColor: 'rgba(54, 162, 235, 1)',
                    data: yourDensity
                },
                {
                    label: 'Competitor',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    pointBackgroundColor: 'rgba(255, 99, 132, 1)',
                    data: competitorDensity
                }
            ]
        },
        options: {
            scales: {
                r: {
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Keyword Density Comparison (%)'
                }
            }
        }
    });
}

/**
 * Creates a bar chart for content metrics
 * @param {string} canvasId - The canvas element ID
 * @param {Object} contentData - The content data object 
 */
function createContentMetricsChart(canvasId, contentData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    return new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: ['Word Count', 'Paragraph Count', 'Sentence Count', 'Readability Score'],
            datasets: [{
                label: 'Content Metrics',
                backgroundColor: [
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(153, 102, 255, 0.7)',
                    'rgba(255, 159, 64, 0.7)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1,
                data: [
                    contentData.word_count,
                    contentData.paragraph_count,
                    contentData.sentence_count,
                    contentData.readability.score
                ]
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Content Metrics'
                }
            }
        }
    });
}
