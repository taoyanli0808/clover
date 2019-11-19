/**
 * 窗口部分
 */
function getCommandHandler() {
    var html = '<div class="command" classify="browser" command="get"><lable>打开网址：</label><input type="url" /></div>';
    return html;
}

function forwardCommandHandler() {
    var html = '<div class="command" classify="browser" command="forward"><lable>前进</label></div>'
    return html;
}

function backCommandHandler() {
    var html = '<div class="command" classify="browser" command="back"><lable>后退</label></div>'
    return html;
}

function refreshCommandHandler() {
    var html = '<div class="command" classify="browser" command="refresh"><lable>刷新</label></div>'
    return html;
}

function quitCommandHandler() {
    var html = '<div class="command" classify="browser" command="quit"><lable>退出</label></div>'
    return html;
}

function switchToFrameCommandHandler() {
    var html = '<div class="command" classify="browser" command="switch_to_frame"><lable>切换Frame：</label><input type="text" /></div>'
    return html;
}

function switchToWindowCommandHandler() {
    var html = '<div class="command" classify="browser" command="switch_to_window"><lable>切换Window：</label><input type="text" /></div>'
    return html;
}

function maximizeWindowCommandHandler() {
    var html = '<div class="command" classify="browser" command="maximize_window"><lable>最大化</label></div>'
    return html;
}

function minimizeWindowCommandHandler() {
    var html = '<div class="command" classify="browser" command="minimize_window"><lable>最小化</label></div>'
    return html;
}

function resizeCommandHandler() {
    var html = '<div class="command" classify="browser" command="minimize_window"><lable>未实现</label></div>'
    return html;
}

/**
 * 选择器部分
 */
function idCommandHandler() {
    var html = '<div class="command" classify="selector" command="find_element_by_id"><lable>ID选择器表达式：</label><input type="text" /></div>';
    return html;
}

function nameCommandHandler() {
    var html = '<div class="command" classify="selector" command="find_element_by_name"><lable>Name选择器表达式：</label><input type="text" /></div>';
    return html;
}

function cssCommandHandler() {
    var html = '<div class="command" classify="selector" command="find_element_by_css_selector"><lable>CSS选择器表达式：</label><input type="text" /></div>';
    return html;
}

function classCommandHandler() {
    var html = '<div class="command" classify="selector" command="find_element_by_class"><lable>类选择器表达式：</label><input type="text" /></div>';
    return html;
}

function xpathCommandHandler() {
    var html = '<div class="command" classify="selector" command="find_element_by_xpath"><lable>Xpath选择器表达式：</label><input type="text" /></div>';
    return html;
}

function tagCommandHandler() {
    var html = '<div class="command" classify="selector" command="find_element_by_tag"><lable>Tag选择器表达式：</label><input type="text" /></div>';
    return html;
}

function linkCommandHandler() {
    var html = '<div class="command" classify="selector" command="find_element_by_link_text"><lable>超链接文本选择器内容：</label><input type="text" /></div>';
    return html;
}

function partialCommandHandler() {
    var html = '<div class="command" classify="selector" command="find_element_by_partial_link_text"><lable>部分超链接文本选择器内容：</label><input type="text" /></div>';
    return html;
}

/**
 * 动作部分
 */
function sendKeysCommandHandler() {
    var html = '<div class="command" classify="action" command="send_keys"><label>输入文本信息：</label><input type="text" placeholder="请在这里输入..." /></div>';
    return html;
}

function clickCommandHandler() {
    var html = '<div class="command" classify="action" command="click"><label>鼠标点击左键</label></div>';
    return html;
}

function contextClickCommandHandler() {
    var html = '<div class="command" classify="action" command="context_click"><label>鼠标点击右键</label></div>';
    return html;
}

function doubleClickCommandHandler() {
    var html = '<div class="command" classify="action" command="double_click"><label>鼠标双击左键</label></div>';
    return html;
}

function dragAndDropCommandHandler() {
    var html = '<div class="command" classify="action" command="drag_and_drop"><label>拖拽元素</label>源：<input />目标：<input></div>';
    return html;
}

function clickAndHoldCommandHandler() {
    var html = '<div class="command" classify="action" command="click_and_hold"><label>点击并保持</label></div>';
    return html;
}

function moveToElementCommandHandler() {
    var html = '<div class="command" classify="action" command="move_to_element"><label>移动到元素位置</label></div>';
    return html;
}

function moveByOffsetCommandHandler() {
    var html = '<div class="command" classify="action" command="move_by_offset"><label>移动一定偏移量：</label><input type="text" placeholder="xoffser"><input type="text" placeholder="yoffser"></div>';
    return html;
}

var commands = {
    'browser': {
        'get': getCommandHandler,
        'forward': forwardCommandHandler,
        'back': backCommandHandler,
        'refresh': refreshCommandHandler,
        'quit': quitCommandHandler,
        'switch_to_frame': switchToFrameCommandHandler,
        'switch_to_window': switchToWindowCommandHandler,
        'maximize_window': maximizeWindowCommandHandler,
        'minimize_window': minimizeWindowCommandHandler,
        'resize': resizeCommandHandler
    },
    'selector': {
        'find_element_by_id': idCommandHandler,
        'find_element_by_name': nameCommandHandler,
        'find_element_by_css_selector': cssCommandHandler,
        'find_element_by_class': classCommandHandler,
        'find_element_by_xpath': xpathCommandHandler,
        'find_element_by_tag': tagCommandHandler,
        'find_element_by_link_text': linkCommandHandler,
        'find_element_by_partial_link_text': partialCommandHandler
    },
    'action': {
        'send_keys': sendKeysCommandHandler,
        'click': clickCommandHandler,
        'context_click': contextClickCommandHandler,
        'double_click': doubleClickCommandHandler,
        'drag_and_drop': dragAndDropCommandHandler,
        'click_and_hold': clickAndHoldCommandHandler,
        'move_to_element': moveToElementCommandHandler,
        'move_by_offset': moveByOffsetCommandHandler
    }
}
