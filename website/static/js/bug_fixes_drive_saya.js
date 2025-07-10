// 🐛 BUG FIXES UNTUK DRIVE SAYA - COMPREHENSIVE SOLUTION
// Fixes for 3 main bugs after cancel operations

console.log('🐛 Loading Drive Saya Bug Fixes...');

// 🐛 BUG FIX 1: Layout Grid Consistency
function fixGridLayoutConsistency() {
    console.log('🔧 Bug Fix 1: Applying consistent grid layout...');
    
    // Create unified CSS for consistent grid layout
    const gridFixCSS = document.createElement('style');
    gridFixCSS.id = 'grid-layout-fix';
    gridFixCSS.innerHTML = `
        /* 🔧 CONSISTENT GRID LAYOUT - Priority untuk kolom nama */
        .file-item,
        [data-name],
        [data-path] {
            display: grid !important;
            grid-template-columns: minmax(350px, 3fr) 150px 120px 100px 40px !important;
            gap: 16px !important;
            align-items: center !important;
            padding: 12px 16px !important;
        }
        
        /* Force nama kolom untuk selalu terlihat */
        .file-item .flex.items-center.gap-2.truncate,
        .file-item > div:first-child {
            min-width: 300px !important;
            flex-shrink: 0 !important;
            flex-grow: 1 !important;
            max-width: none !important;
            overflow: visible !important;
        }
        
        /* 🐛 AGGRESSIVE MOBILE FIX untuk selected items */
        @media (max-width: 768px) {
            .file-item,
            [data-name],
            [data-path] {
                grid-template-columns: minmax(150px, 3fr) 80px 60px 40px !important;
                gap: 8px !important;
                padding: 8px !important;
                font-size: 13px !important;
            }
            
            /* 🐛 ULTRA PRIORITAS: Selected items di mobile */
            .file-item.direct-selected,
            [data-name].direct-selected,
            [data-path].direct-selected {
                grid-template-columns: 1fr 60px 30px !important;
                gap: 4px !important;
                padding: 6px 8px !important;
                margin: 2px 0 !important;
            }
            
            /* Kolom nama MAKSIMAL prioritas untuk selected items */
            .file-item.direct-selected .flex.items-center.gap-2.truncate,
            .file-item.direct-selected > div:first-child {
                min-width: 0 !important;
                width: 100% !important;
                max-width: none !important;
                overflow: visible !important;
                flex-shrink: 0 !important;
                flex-grow: 1 !important;
                position: relative !important;
                z-index: 10 !important;
                margin-right: 8px !important;
            }
            
            /* Text nama file DOMINAN di mobile */
            .file-item.direct-selected .text-sm.text-gray-900.truncate,
            .file-item.direct-selected .file-name {
                white-space: nowrap !important;
                overflow: visible !important;
                text-overflow: unset !important;
                width: 100% !important;
                font-weight: 700 !important;
                color: #0d47a1 !important;
                font-size: 14px !important;
                line-height: 1.2 !important;
            }
            
            /* HIDE semua kolom kecuali nama dan action untuk selected */
            .file-item.direct-selected > div:nth-child(2),
            .file-item.direct-selected > div:nth-child(3),
            .file-item.direct-selected > div:nth-child(4) {
                display: none !important;
            }
            
            /* Keep only last column (actions) visible but minimal */
            .file-item.direct-selected > div:last-child {
                width: 30px !important;
                min-width: 30px !important;
                flex-shrink: 0 !important;
            }
            
            /* Selected item styling optimized for mobile */
            .file-item.direct-selected {
                background: linear-gradient(135deg, #e3f2fd, #bbdefb) !important;
                border: 2px solid #1976d2 !important;
                border-radius: 8px !important;
                box-shadow: 0 2px 8px rgba(25, 118, 210, 0.3) !important;
            }
        }
        
        /* Extreme mobile responsive (≤ 480px) */
        @media (max-width: 480px) {
            .file-item,
            [data-name],
            [data-path] {
                grid-template-columns: 1fr 40px !important;
                gap: 4px !important;
                padding: 6px !important;
                font-size: 12px !important;
            }
            
            /* ULTRA MINIMAL untuk selected di extreme mobile */
            .file-item.direct-selected,
            [data-name].direct-selected,
            [data-path].direct-selected {
                grid-template-columns: 1fr 25px !important;
                gap: 2px !important;
                padding: 4px 6px !important;
                margin: 1px 0 !important;
            }
            
            /* Hide ALL columns except name dan minimal action */
            .file-item > div:nth-child(2),
            .file-item > div:nth-child(3),
            .file-item > div:nth-child(4),
            .file-item > div:nth-child(5) {
                display: none !important;
            }
            
            .file-item.direct-selected > div:nth-child(2),
            .file-item.direct-selected > div:nth-child(3),
            .file-item.direct-selected > div:nth-child(4) {
                display: none !important;
            }
            
            /* Action button minimal di extreme mobile */
            .file-item.direct-selected > div:last-child {
                width: 25px !important;
                min-width: 25px !important;
            }
            
            .file-item.direct-selected > div:last-child button {
                width: 20px !important;
                height: 20px !important;
                padding: 2px !important;
            }
            
            /* Font super kecil untuk extreme mobile */
            .file-item.direct-selected .text-sm.text-gray-900.truncate,
            .file-item.direct-selected .file-name {
                font-size: 12px !important;
                font-weight: 600 !important;
            }
        }
        
        /* Header table juga konsisten */
        #table-header {
            display: grid !important;
            grid-template-columns: minmax(350px, 3fr) 150px 120px 100px 40px !important;
            gap: 16px !important;
            align-items: center !important;
        }
        
        @media (max-width: 768px) {
            #table-header {
                grid-template-columns: minmax(150px, 3fr) 80px 60px 40px !important;
                gap: 8px !important;
                padding: 8px !important;
                font-size: 11px !important;
            }
            
            /* Hide some header columns in mobile */
            #table-header > div:nth-child(3),
            #table-header > div:nth-child(4) {
                display: none !important;
            }
        }
        
        @media (max-width: 480px) {
            #table-header {
                grid-template-columns: 1fr 40px !important;
                gap: 4px !important;
                padding: 6px !important;
                font-size: 10px !important;
            }
            
            /* Hide most header columns in extreme mobile */
            #table-header > div:nth-child(2),
            #table-header > div:nth-child(3),
            #table-header > div:nth-child(4),
            #table-header > div:nth-child(5) {
                display: none !important;
            }
        }
    `;
    
    // Remove existing grid fix if exists
    const existingFix = document.getElementById('grid-layout-fix');
    if (existingFix) existingFix.remove();
    
    document.head.appendChild(gridFixCSS);
    console.log('✅ Grid layout consistency applied');
}

// 🐛 BUG FIX 1B: AGGRESSIVE Responsive Layout for Selected Items
function fixResponsiveSelectedItems() {
    console.log('📱 Applying AGGRESSIVE responsive fixes for selected items...');
    
    // Force apply responsive layout specifically for selected items
    const selectedItems = document.querySelectorAll('.direct-selected');
    selectedItems.forEach(item => {
        // Force re-calculation of layout
        item.style.display = 'none';
        item.offsetHeight; // Force reflow
        item.style.display = 'grid';
        
        // Detect screen size
        const isNarrow = window.innerWidth <= 768;
        const isExtremeNarrow = window.innerWidth <= 480;
        
        // Apply ULTRA aggressive grid layout
        if (isExtremeNarrow) {
            item.style.gridTemplateColumns = '1fr 25px';
            item.style.gap = '2px';
            item.style.padding = '4px 6px';
            item.style.margin = '1px 0';
        } else if (isNarrow) {
            item.style.gridTemplateColumns = '1fr 60px 30px';
            item.style.gap = '4px';
            item.style.padding = '6px 8px';
            item.style.margin = '2px 0';
        } else {
            // Reset to normal for desktop
            item.style.gridTemplateColumns = '';
            item.style.gap = '';
            item.style.padding = '';
            item.style.margin = '';
        }
        
        // ULTRA prioritize name column in mobile
        const nameContainer = item.querySelector('.flex.items-center.gap-2.truncate') || 
                             item.querySelector('div:first-child');
        if (nameContainer && isNarrow) {
            nameContainer.style.minWidth = '0';
            nameContainer.style.width = '100%';
            nameContainer.style.overflow = 'visible';
            nameContainer.style.flexShrink = '0';
            nameContainer.style.flexGrow = '1';
            nameContainer.style.zIndex = '10';
            nameContainer.style.marginRight = '8px';
            
            // Apply to filename text as well
            const fileNameText = nameContainer.querySelector('.text-sm.text-gray-900.truncate') ||
                                nameContainer.querySelector('.file-name') ||
                                nameContainer.querySelector('span:last-child');
            if (fileNameText) {
                fileNameText.style.whiteSpace = 'nowrap';
                fileNameText.style.overflow = 'visible';
                fileNameText.style.textOverflow = 'unset';
                fileNameText.style.width = '100%';
                fileNameText.style.fontWeight = '700';
                fileNameText.style.color = '#0d47a1';
                fileNameText.style.fontSize = isExtremeNarrow ? '12px' : '14px';
                fileNameText.style.lineHeight = '1.2';
            }
        }
        
        // Hide columns for mobile selected items
        if (isNarrow) {
            const columns = item.querySelectorAll(':scope > div');
            columns.forEach((col, index) => {
                if (index >= 1 && index < columns.length - 1) {
                    col.style.display = 'none';
                }
            });
            
            // Keep last column minimal for actions
            const lastCol = columns[columns.length - 1];
            if (lastCol) {
                lastCol.style.width = isExtremeNarrow ? '25px' : '30px';
                lastCol.style.minWidth = isExtremeNarrow ? '25px' : '30px';
                lastCol.style.flexShrink = '0';
                
                // Minimize action button
                const button = lastCol.querySelector('button');
                if (button && isExtremeNarrow) {
                    button.style.width = '20px';
                    button.style.height = '20px';
                    button.style.padding = '2px';
                }
            }
        }
    });
    
    console.log(`✅ AGGRESSIVE responsive fixes applied to ${selectedItems.length} selected items`);
}

// 🐛 BUG FIX 2: Enhanced Force Repaint System
function enhancedForceRepaint(element) {
    if (!element) return;
    
    // Method 1: Display manipulation
    const originalDisplay = element.style.display;
    element.style.display = 'none';
    element.offsetHeight; // Force reflow
    element.style.display = originalDisplay || '';
    
    // Method 2: Transform trigger
    element.style.transform = 'translate3d(0,0,0)';
    element.offsetHeight; // Force reflow
    element.style.transform = '';
    
    // Method 3: Opacity flash
    const originalOpacity = element.style.opacity;
    element.style.opacity = '0.99';
    element.offsetHeight; // Force reflow
    element.style.opacity = originalOpacity || '1';
    
    // Method 4: Class manipulation
    element.classList.add('repaint-trigger');
    element.offsetHeight; // Force reflow
    element.classList.remove('repaint-trigger');
    
    // Method 5: Force style recalculation
    window.getComputedStyle(element).getPropertyValue('opacity');
}

// 🐛 BUG FIX 2: Global repaint for all elements
function globalForceRepaint() {
    console.log('🎨 Bug Fix 2: Applying global force repaint...');
    
    // Repaint body
    document.body.style.transform = 'translate3d(0,0,0)';
    document.body.offsetHeight;
    document.body.style.transform = '';
    
    // Repaint all file items
    const fileItems = document.querySelectorAll('.file-item, [data-name], [data-path]');
    fileItems.forEach(element => {
        enhancedForceRepaint(element);
    });
    
    console.log('✅ Global force repaint completed');
}

// 🐛 BUG FIX 3: Enhanced Context Menu Reattachment
function reattachAllEventListeners() {
    console.log('🔗 Bug Fix 3: Reattaching all event listeners...');
    
    const fileItems = document.querySelectorAll('.file-item, [data-name], [data-path]');
    
    fileItems.forEach((item, index) => {
        const fileName = item.getAttribute('data-name') || 
                        item.getAttribute('data-path') || 
                        `item-${index}`;
        
        // Clean slate approach: clone element to remove all existing listeners
        const newItem = item.cloneNode(true);
        if (item.parentNode) {
            item.parentNode.replaceChild(newItem, item);
        }
        
        // Re-add CTRL+Click listener
        newItem.addEventListener('click', function(e) {
            if (e.ctrlKey || e.metaKey) {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                
                console.log('🖱️ CTRL+Click on:', fileName);
                
                // Toggle selection
                if (newItem.classList.contains('direct-selected')) {
                    // Deselect
                    newItem.classList.remove('direct-selected');
                    if (window.directSelected) {
                        window.directSelected.delete(fileName);
                    }
                } else {
                    // Select
                    newItem.classList.add('direct-selected');
                    if (!window.directSelected) {
                        window.directSelected = new Set();
                    }
                    window.directSelected.add(fileName);
                }
                
                // Apply enhanced repaint
                enhancedForceRepaint(newItem);
                
                // Update counter
                updateSelectionCounter();
                
                return false;
            }
        }, true);
        
        // Re-add right-click context menu listener
        newItem.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            
            console.log('🖱️ Right-click on:', fileName);
            
            // Show context menu
            showContextMenu(e, newItem, fileName);
            
            return false;
        }, true);
        
        // Re-add double-click listener
        newItem.addEventListener('dblclick', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            console.log('🖱️ Double-click on:', fileName);
            // Handle file/folder opening
            const itemType = newItem.getAttribute('data-type') || 'file';
            if (itemType === 'folder') {
                // Navigate to folder
                window.location.href = `/?path=${encodeURIComponent(fileName)}`;
            } else {
                // Open file
                const filePath = newItem.getAttribute('data-path') || fileName;
                window.open(`/file?path=${encodeURIComponent(filePath)}`, '_blank');
            }
        });
    });
    
    console.log(`✅ Event listeners reattached for ${fileItems.length} items`);
}

// 🐛 UTILITY: Update selection counter
function updateSelectionCounter() {
    const count = window.directSelected ? window.directSelected.size : 0;
    const selectedCountEl = document.getElementById('selected-count-header');
    const notificationBar = document.getElementById('selection-notification-bar');
    
    if (selectedCountEl) {
        selectedCountEl.textContent = count;
    }
    
    if (notificationBar) {
        if (count > 0) {
            notificationBar.style.display = 'block';
            notificationBar.style.visibility = 'visible';
            notificationBar.style.opacity = '1';
        } else {
            notificationBar.style.display = 'none';
            notificationBar.style.visibility = 'hidden';
            notificationBar.style.opacity = '0';
        }
    }
    
    // 🐛 RESPONSIVE FIX: Apply responsive layout after selection changes
    setTimeout(() => {
        fixResponsiveSelectedItems();
    }, 50);
}

// 🐛 UTILITY: Simple context menu
function showContextMenu(event, element, fileName) {
    // Remove existing context menus
    document.querySelectorAll('.custom-context-menu').forEach(menu => menu.remove());
    
    const contextMenu = document.createElement('div');
    contextMenu.className = 'custom-context-menu';
    contextMenu.style.cssText = `
        position: fixed;
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 999999;
        padding: 8px 0;
        min-width: 180px;
        font-size: 14px;
    `;
    
    const menuItems = [
        { text: '📁 Buka', action: () => console.log('Open:', fileName) },
        { text: '✏️ Rename', action: () => console.log('Rename:', fileName) },
        { text: '📋 Salin', action: () => console.log('Copy:', fileName) },
        { text: '✂️ Potong', action: () => console.log('Cut:', fileName) },
        { text: '🗑️ Hapus', action: () => console.log('Delete:', fileName) },
        { text: '🔵 Pilih', action: () => {
            // Toggle selection
            if (element.classList.contains('direct-selected')) {
                element.classList.remove('direct-selected');
                if (window.directSelected) {
                    window.directSelected.delete(fileName);
                }
            } else {
                element.classList.add('direct-selected');
                if (!window.directSelected) {
                    window.directSelected = new Set();
                }
                window.directSelected.add(fileName);
            }
            enhancedForceRepaint(element);
            updateSelectionCounter();
            contextMenu.remove();
        }}
    ];
    
    menuItems.forEach(item => {
        const menuItem = document.createElement('div');
        menuItem.textContent = item.text;
        menuItem.style.cssText = `
            padding: 8px 16px;
            cursor: pointer;
            transition: background-color 0.2s;
        `;
        menuItem.addEventListener('mouseenter', () => {
            menuItem.style.backgroundColor = '#f3f4f6';
        });
        menuItem.addEventListener('mouseleave', () => {
            menuItem.style.backgroundColor = '';
        });
        menuItem.addEventListener('click', () => {
            item.action();
            contextMenu.remove();
        });
        contextMenu.appendChild(menuItem);
    });
    
    document.body.appendChild(contextMenu);
    
    // Position menu
    contextMenu.style.left = event.pageX + 'px';
    contextMenu.style.top = event.pageY + 'px';
    
    // Close menu when clicking outside
    setTimeout(() => {
        document.addEventListener('click', function closeMenu(e) {
            if (!contextMenu.contains(e.target)) {
                contextMenu.remove();
                document.removeEventListener('click', closeMenu);
            }
        });
    }, 0);
}

// 🐛 MAIN COMPREHENSIVE FIX FUNCTION
function comprehensiveBugFix() {
    console.log('\n🐛🐛🐛 COMPREHENSIVE BUG FIX STARTING...');
    
    // Apply all fixes
    fixGridLayoutConsistency();
    globalForceRepaint();
    reattachAllEventListeners();
    
    // Initialize selection system
    if (!window.directSelected) {
        window.directSelected = new Set();
    }
    
    // Setup cancel button
    const cancelBtn = document.getElementById('cancel-select-btn');
    if (cancelBtn) {
        // Clean slate approach for cancel button
        const newCancelBtn = cancelBtn.cloneNode(true);
        cancelBtn.parentNode.replaceChild(newCancelBtn, cancelBtn);
        
        newCancelBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            
            console.log('\n❌ CANCEL BUTTON CLICKED - APPLYING COMPREHENSIVE FIXES...');
            
            // Clear all selections
            document.querySelectorAll('.direct-selected').forEach(el => {
                el.classList.remove('direct-selected');
                enhancedForceRepaint(el);
            });
            
            if (window.directSelected) {
                window.directSelected.clear();
            }
            
            updateSelectionCounter();
            
            // Apply all fixes after cancel
            setTimeout(() => {
                fixGridLayoutConsistency();
                globalForceRepaint();
                reattachAllEventListeners();
                console.log('✅ All bug fixes applied after cancel');
            }, 100);
            
            return false;
        }, true);
        
        console.log('✅ Cancel button fixed');
    }
    
    // Setup CTRL+A functionality
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'a') {
            e.preventDefault();
            
            const fileItems = document.querySelectorAll('.file-item, [data-name], [data-path]');
            if (!window.directSelected) {
                window.directSelected = new Set();
            }
            
            fileItems.forEach(item => {
                const fileName = item.getAttribute('data-name') || 
                               item.getAttribute('data-path') || 
                               'unknown';
                item.classList.add('direct-selected');
                window.directSelected.add(fileName);
                enhancedForceRepaint(item);
            });
            
            updateSelectionCounter();
            console.log('✅ CTRL+A applied');
        }
    });
    
    // 🐛 RESPONSIVE FIX: Window resize listener
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            console.log('📱 Window resized, applying responsive fixes...');
            fixResponsiveSelectedItems();
            fixGridLayoutConsistency();
        }, 150);
    });
    
    // 🐛 FORCE IMMEDIATE RESPONSIVE APPLICATION
    setTimeout(() => {
        fixResponsiveSelectedItems();
        console.log('🔄 Force applied responsive fixes for any existing selections');
    }, 200);
    
    console.log('✅✅✅ COMPREHENSIVE BUG FIX COMPLETED');
    console.log('🎯 All 4 bugs should now be fixed:');
    console.log('  1. ✅ Grid layout konsisten');
    console.log('  2. ✅ Highlight biru akan muncul');
    console.log('  3. ✅ Context menu akan berfungsi');
    console.log('  4. ✅ AGGRESSIVE mobile responsive untuk selected items');
}

// 🐛 AUTO-APPLY FIXES WHEN DOM IS READY
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', comprehensiveBugFix);
} else {
    comprehensiveBugFix();
}

// 🐛 EXPOSE FUNCTIONS GLOBALLY FOR TESTING
window.driveSayaFixes = {
    comprehensiveBugFix,
    fixGridLayoutConsistency,
    fixResponsiveSelectedItems,
    globalForceRepaint,
    reattachAllEventListeners,
    enhancedForceRepaint,
    updateSelectionCounter
};

console.log('🐛 Drive Saya Bug Fixes loaded successfully');
console.log('🧪 Test functions available: window.driveSayaFixes');