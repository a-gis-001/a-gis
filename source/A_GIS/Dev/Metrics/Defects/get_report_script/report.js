// List of allowed products.
const PRODUCTS = {{ products | tojson }};

// List of severity descriptions.
const SEVERITY_DESCRIPTIONS = {
    {% for name, level in severity.items() %}
    "{{ name }}": "{{ level.description }}. (weight={{ level.allowed_weights|join('/') }})"{% if not loop.last %},{% endif %}
    {% endfor %}
};

// The checkbox state is the only state.
const CHECKBOX_STATES = {
    idOnly: {
        {% for name, level in severity.items() %}
        '{{ name }}': {{ level.defaultIdOnly|tojson }}{% if not loop.last %},{% endif %}
        {% endfor %}
    },
    showDesc: {
        {% for name, level in severity.items() %}
        '{{ name }}': {{ level.defaultShowDesc|tojson }}{% if not loop.last %},{% endif %}
        {% endfor %}
    },
    hideAll: {
        {% for name, level in severity.items() %}
        '{{ name }}': {{ level.defaultHideAll|tojson }}{% if not loop.last %},{% endif %}
        {% endfor %}
    }
};

// This list of issues is initialized once.
let ISSUES = [];

// Event listeners are public functions.
document.addEventListener('DOMContentLoaded', () => {
    initializeLayout();
    ISSUES = parseIssues(SEVERITY_DESCRIPTIONS);
    createProductFilter(SEVERITY_DESCRIPTIONS, PRODUCTS, ISSUES, CHECKBOX_STATES);
    createContentListing(SEVERITY_DESCRIPTIONS, ISSUES, CHECKBOX_STATES);
    addStandalonePageButtons();
    addBlockCopyButtons();
});

// NOTE on organization:
// Top-level utility functions use __ prefix. Nested 
// functions inside public functions use _ prefix.

// Create a generic checkbox.
function __createCheckbox(id, labelText, checked = false) {
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = id;
    checkbox.checked = checked;

    const label = document.createElement('label');
    label.htmlFor = id;
    label.textContent = labelText;

    return { checkbox, label };
}

// Create an issue list item.
function __createListItem(issue, showIdOnly, showDesc) {
    const li = document.createElement('li');

    const a = document.createElement('a');

    a.href = `#${issue.id}`;
    const titleSpan = document.createElement('span');
    titleSpan.style.fontWeight = 'bold';
    titleSpan.textContent = showIdOnly ? issue.id : issue.title;

    a.appendChild(titleSpan);

    if (showDesc) {
        const descSpan = document.createElement('span');
        descSpan.style.fontWeight = 'normal';
        descSpan.textContent = `  ·  ${issue.description} (weight=${issue.weight})`;
        a.appendChild(descSpan);
        li.style.display = 'block';
        li.style.marginBottom = '0.5em';
    } else {
        li.style.display = 'inline-block';
        li.removeAttribute('title');
        li.setAttribute('data-tooltip', issue.description);
    }

    li.className = `defect-${issue.severity}`;
    li.appendChild(a);
    return li;
}

// Extract the page style.
function __extractPageStyle() {
    const styleElements = document.querySelectorAll('style');
    return Array.from(styleElements)
        .map(style => style.innerHTML)
        .join('\n');
}

// Create the controls.
function __createControls(severityLevel, states) {
    const controls = document.createElement('div');
    controls.className = 'controls';

    const { checkbox: idCheckbox, label: idLabel } = __createCheckbox(
        `idOnly-${severityLevel}`,
        'ID only',
        states.idOnly[severityLevel] || false
    );
    const { checkbox: descCheckbox, label: descLabel } = __createCheckbox(
        `showDesc-${severityLevel}`,
        'Include description',
        states.showDesc[severityLevel] || false
    );
    const { checkbox: hideCheckbox, label: hideLabel } = __createCheckbox(
        `hide-${severityLevel}`,
        'Hide all',
        states.hideAll[severityLevel] || false
    );

    controls.appendChild(idCheckbox);
    controls.appendChild(idLabel);
    controls.appendChild(descCheckbox);
    controls.appendChild(descLabel);
    controls.appendChild(hideCheckbox);
    controls.appendChild(hideLabel);

    return { controls, idCheckbox, descCheckbox, hideCheckbox };
}

// Update a list.
function __updateList(ul, issues, showIdOnly, showDesc, hideAll) {
    ul.innerHTML = '';
    if (hideAll) {
        return;
    }
    issues.forEach(issue => {
        const li = __createListItem(issue, showIdOnly, showDesc);
        ul.appendChild(li);
    });
}

// Create a severity block.
function __createSeverityBlock(severityDescriptions, severityLevel, issues, states) {
    const section = document.createElement('div');
    section.style.marginBottom = '10px';

    const headerContainer = document.createElement('div');
    const header = document.createElement('h3');
    header.style.margin = '0';
    header.className = `defect-${severityLevel}`;
    header.title = severityDescriptions[severityLevel];
    header.textContent = `${severityLevel} (${issues.length})`;

    const description = document.createElement('div');
    description.style.fontSize = '0.9em';
    description.style.color = '#666';
    description.style.marginBottom = '10px';
    description.textContent = severityDescriptions[severityLevel];

    headerContainer.appendChild(header);
    headerContainer.appendChild(description);
    section.appendChild(headerContainer);

    const { controls, idCheckbox, descCheckbox, hideCheckbox } = __createControls(severityLevel, states);
    section.appendChild(controls);

    const ul = document.createElement('ul');
    section.appendChild(ul);

    const _updateListWithState = () => {
        states.idOnly[severityLevel] = idCheckbox.checked;
        states.showDesc[severityLevel] = descCheckbox.checked;
        states.hideAll[severityLevel] = hideCheckbox.checked;
        __updateList(ul, issues, idCheckbox.checked, descCheckbox.checked, hideCheckbox.checked);
        __updateSectionVisibility(document.getElementById('product-filter').value, states);
        __updateSidebarNav(); 
    };
    idCheckbox.addEventListener('change', _updateListWithState);
    descCheckbox.addEventListener('change', _updateListWithState);
    hideCheckbox.addEventListener('change', _updateListWithState);

    _updateListWithState();
    return section;
}

// Update sidebar navigation.
function __updateSidebarNav() {
    const sidebar = document.getElementById('sidebar-nav');
    sidebar.innerHTML = '';

    const ul = document.createElement('ul');
    document.querySelectorAll('h2').forEach(h2 => {
        if (h2.closest('section').style.display !== 'none') {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = `#${h2.id}`;
            a.textContent = h2.textContent;
            a.className = h2.className;
            li.appendChild(a);
            ul.appendChild(li);
        }
    });

    sidebar.appendChild(ul);
}

// Initialize the layout.
function initializeLayout() {
    function _createLeftContainer() {
        const container = document.createElement('div');
        container.style.position = 'sticky';
        container.style.top = '0';
        container.style.maxHeight = '100vh';
        container.style.display = 'flex';
        container.style.flexDirection = 'column';
        return container;
    }

    function _createHomeContainer() {
        const container = document.createElement('div');
        container.id = 'sidebar-home';
        container.style.border = 'var(--root-border)';
        container.style.borderRadius = 'var(--root-border-radius)';
        container.style.padding = 'var(--root-padding)';
        container.style.margin = 'var(--root-margin)';
        container.style.marginBottom = '10px';
        container.style.backgroundColor = 'lightgrey';

        const homeLink = document.createElement('a');
        homeLink.href = '#';
        homeLink.style.display = 'flex';
        homeLink.style.justifyContent = 'center';
        homeLink.style.textDecoration = 'none';
        homeLink.style.color = 'inherit';
        homeLink.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>`;

        container.appendChild(homeLink);
        return container;
    }

    function _createSidebarContainer() {
        const container = document.createElement('div');
        container.id = 'sidebar-nav';
        container.style.width = 'auto';
        container.style.flexShrink = '0';
        container.style.overflowY = 'auto';
        container.style.border = 'var(--root-border)';
        container.style.borderRadius = 'var(--root-border-radius)';
        container.style.padding = 'var(--root-padding)';
        container.style.flex = '1';
        return container;
    }

    const originalContent = document.getElementById('content');
    const contentClone = originalContent.cloneNode(true);
    originalContent.remove();

    const mainContainer = document.createElement('div');
    mainContainer.style.display = 'flex';
    mainContainer.style.gap = '20px';
    mainContainer.style.padding = '20px';

    const leftContainer = _createLeftContainer();
    const homeContainer = _createHomeContainer();
    const sidebarContainer = _createSidebarContainer();

    leftContainer.appendChild(homeContainer);
    leftContainer.appendChild(sidebarContainer);

    const contentWrapper = document.createElement('div');
    contentWrapper.style.flex = '1';
    contentWrapper.style.minWidth = '0';
    contentWrapper.style.overflowX = 'auto';
    contentWrapper.appendChild(contentClone);

    mainContainer.appendChild(leftContainer);
    mainContainer.appendChild(contentWrapper);
    document.body.appendChild(mainContainer);
}

// Parse issues from the sections.
function parseIssues(severityDescriptions) {
    const sections = document.querySelectorAll('section');
    return Array.from(sections).map(section => {
        const h2 = section.querySelector('h2');
        const id = h2.getAttribute('id');
        const title = h2.textContent.trim();

        // Requires a special span used to isolate the severity name in
        // the HTML. For example, if you have a MINIOR severity level, then
        // you should have this span in your HTML to enable the tooltip.
        // <span class="tooltip-MINOR">MINOR</span>
        const severitySpan = section.querySelector('span[class^="tooltip-"]');
        if (severitySpan) {
            severitySpan.removeAttribute('title');
            severitySpan.setAttribute('data-tooltip', severityDescriptions[severitySpan.textContent]);
        }
        const severity = severitySpan ? severitySpan.textContent : '';

        // Similarly, extracting the weight requires a specific span.
        const weight = section.querySelector('.weight').textContent;

        // Extracting the products also requires a specific span.
        const productsSpan = section.querySelector('.products');
        const products = productsSpan ? productsSpan.textContent.split(', ') : [];

        const descriptionH3 = Array.from(section.querySelectorAll('h3'))
            .find(h3 => h3.textContent === 'Description');
        const description = descriptionH3 ?
            descriptionH3.nextElementSibling.textContent : '';

        return { id, title, severity, weight: parseInt(weight), description, products };
    });
}

function __updateSectionVisibility(selectedProduct, states) {
    document.querySelectorAll('section').forEach(section => {
        const productsSpan = section.querySelector('.products');
        const severitySpan = section.querySelector('span[class^="tooltip-"]');
        const severityLevel = severitySpan ? severitySpan.textContent : '';

        const productMatch = selectedProduct === 'All' ||
            (productsSpan && productsSpan.textContent.includes(selectedProduct));

        section.style.display = (productMatch && !states.hideAll[severityLevel]) ? '' : 'none';
    });
}

// Create product filter.
function createProductFilter(severityDescriptions, products, issues, states) {
    function _filterIssuesByProduct(selectedProduct, issues) {
        return selectedProduct === 'All' ?
            issues :
            issues.filter(issue => issue.products.includes(selectedProduct));
    }
    const select = document.createElement('select');
    select.id = 'product-filter';

    products.forEach(product => {
        const option = document.createElement('option');
        option.value = product;
        option.textContent = product;
        select.appendChild(option);
    });

    select.addEventListener('change', (event) => {
        const selectedProduct = event.target.value;
        const filteredIssues = _filterIssuesByProduct(selectedProduct, issues);
        __updateSectionVisibility(selectedProduct, states);
        createContentListing(severityDescriptions, filteredIssues, states);
    });

    const container = document.getElementById('dropdown-container');
    container.appendChild(select);
}

// Create a content listing.
function createContentListing(severityDescriptions, issues, states) {

    const inlineToc = document.getElementById("inline-toc");
    if( !inlineToc ){
        // Turn off all hide all if we don't show the controls.
        for (let key in states.hideAll) {
            states.hideAll[key] = false;
        }        
        __updateSectionVisibility(document.getElementById('product-filter').value, states);
        __updateSidebarNav(); 
        return
    }

    inlineToc.innerHTML = '';

    const groupedIssues = Object.keys(severityDescriptions).reduce((acc, key) => {
        acc[key] = issues.filter(issue => issue.severity === key)
            .sort((a, b) => b.weight - a.weight);
        return acc;
    }, {});

    Object.keys(severityDescriptions).forEach(severityLevel => {
        const section = __createSeverityBlock(severityDescriptions, severityLevel, groupedIssues[severityLevel], states);
        section.className = 'severity-box';
        inlineToc.appendChild(section);
    });
}

function getKatexBlock() {
    const katexElements = document.querySelectorAll('[data-katex]');
    return Array.from(katexElements).map(el => el.outerHTML).join("\n");
}


// Add standalone page generation buttons to each section.
function addStandalonePageButtons() {
    function _generateStandalonePage(section) {
        const styles = __extractPageStyle();
		const katexBlock = getKatexBlock();  // Get KaTeX HTML from main page
        const html = `<!DOCTYPE html>
<html>
<head>
${katexBlock}
<style>
${styles}
.page-button {
	display: none;
}
</style>

</head>
<body>

${section.outerHTML}

<script>
${addBlockCopyButtons.toString()}
addBlockCopyButtons();
</`+`script>

</body>
</html>`;

        // Create download link
        const link = document.createElement('a');
        link.download = `${section.querySelector('h2').id}.html`;
        const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
        link.href = URL.createObjectURL(blob);
        
        // Trigger download and cleanup
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        setTimeout(() => URL.revokeObjectURL(link.href), 100);
    }

    document.querySelectorAll('section').forEach(section => {
        const h2 = section.querySelector('h2');
        if (h2) {
            const button = document.createElement('button');
            button.className = 'page-button';
            button.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>`;
            button.title = 'Download section';
            button.addEventListener('click', () => _generateStandalonePage(section));
            h2.style.position = 'relative';
            h2.appendChild(button);
        }
    });
}

// Add copy buttons to each block.
function addBlockCopyButtons() {

    document.querySelectorAll('.copy-button').forEach(btn => {
        const wrapper = btn.closest('div');
        if (wrapper) {
            const pre = wrapper.querySelector('pre');
            if (pre) {
                wrapper.parentNode.insertBefore(pre, wrapper);
                wrapper.remove();
            }
        }
    });

    document.querySelectorAll('pre').forEach(pre => {
        // Create wrapper div
        const wrapper = document.createElement('div');
        wrapper.style.position = 'relative';  // For absolute positioning of button
        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(pre);

        const button = document.createElement('button');
        button.className = 'copy-button';
        const originalSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>`;
        button.innerHTML = originalSvg;
        button.title = 'Copy to clipboard';

        button.addEventListener("click", async () => {
            try {
                await navigator.clipboard.writeText(pre.innerText);
                button.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
                setTimeout(() => {
                    button.innerHTML = originalSvg;
                }, 2000);
            } catch (err) {
                console.error("Error copying code:", err);
            }
        });

        wrapper.appendChild(button);
    });
}

