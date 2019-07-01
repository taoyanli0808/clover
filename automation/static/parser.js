
function getCommandParser(index) {
    return {"url": $('.command').eq(index).find("input").val()}
}

function forwardCommandParser(index) {
    return {}
}

function backCommandParser(index) {
    return {}
}

function refreshCommandParser(index) {
    return {}
}

function quitCommandParser(index) {
    return {}
}

function switchToFrameCommandParser(index) {
    return {"selector": $('.command').eq(index).find("input").val()}
}

function switchToWindowCommandParser(index) {
    return {"selector": $('.command').eq(index).find("input").val()}
}

function maximizeWindowCommandParser(index) {
    return {}
}

function minimizeWindowCommandParser(index) {
    return {}
}

function resizeCommandParser(index) {
    return {}
}

function idCommandParser(index) {
    return {"selector": $('.command').eq(index).find("input").val()}
}

function nameCommandParser(index) {
    return {"selector": $('.command').eq(index).find("input").val()}
}

function cssCommandParser(index) {
    return {"selector": $('.command').eq(index).find("input").val()}
}

function classCommandParser(index) {
    return {"selector": $('.command').eq(index).find("input").val()}
}

function xpathCommandParser(index) {
    // console.log($(this).val())
    return {"selector": $('.command').eq(index).find("input").val()}
}

function tagCommandParser(index) {
    return {"selector": $('.command').eq(index).find("input").val()}
}

function linkCommandParser(index) {
    return {"selector": $('.command').eq(index).find("input").val()}
}

function partialCommandParser(index) {
    return {"selector": $('.command').eq(index).find("input").val()}
}

function sendKeysCommandParser(index) {
    return {"selector": $('.command').eq(index).find("input").val()}
}

function clickCommandParser(index) {
    return {}
}

function contextClickCommandParser(index) {
    return {}
}

function doubleClickCommandParser(index) {
    return {}
}

function dragAndDropCommandParser(index) {

}

function clickAndHoldCommandParser(index) {

}

function moveToElementCommandParser(index) {

}

function moveByOffsetCommandParser(index) {

}

var parsers = {
    'browser': {
        'get': getCommandParser,
        'forward': forwardCommandParser,
        'back': backCommandParser,
        'refresh': refreshCommandParser,
        'quit': quitCommandParser,
        'switch_to_frame': switchToFrameCommandParser,
        'switch_to_window': switchToWindowCommandParser,
        'maximize_window': maximizeWindowCommandParser,
        'minimize_window': minimizeWindowCommandParser,
        'resize': resizeCommandParser
    },
    'selector': {
        'find_element_by_id': idCommandParser,
        'find_element_by_name': nameCommandParser,
        'find_element_by_css_selector': cssCommandParser,
        'find_element_by_class': classCommandParser,
        'find_element_by_xpath': xpathCommandParser,
        'find_element_by_tag': tagCommandParser,
        'find_element_by_link_text': linkCommandParser,
        'find_element_by_partial_link_text': partialCommandParser
    },
    'action': {
        'send_keys': sendKeysCommandParser,
        'click': clickCommandParser,
        'context_click': contextClickCommandParser,
        'double_click': doubleClickCommandParser,
        'drag_and_drop': dragAndDropCommandParser,
        'click_and_hold': clickAndHoldCommandParser,
        'move_to_element': moveToElementCommandParser,
        'move_by_offset': moveByOffsetCommandParser
    }
}

/**
 * parser用于遍历所有指令，并解析指令关键信息，保存到commands数组。
 */
function parser() {
    var commands = [];
    $('.command').each(function (index, element) {
        // console.log($('.command').eq(index).attr('classify'))
        var classify = $('.command').eq(index).attr('classify')
        // console.log($('.command').eq(index).attr('command'))
        var command = $('.command').eq(index).attr('command')
        var parameter = parsers[classify][command](index)
        commands.push({
            'classify': classify,
            'command': command,
            'parameter': parameter
        })
    })
    console.log(commands)
    return commands
}