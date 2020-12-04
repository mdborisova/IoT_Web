let $button = $("#button-on-off")[0]
let $battery_power_im = $("#battery")[0].getElementsByClassName('power')[0]
let $battery_power_num = $("#battery_power_num")[0]
let $thermometers = $(".thermometer-class");

const config = {
  minTemp: -20,
  maxTemp: 50
};

function update_battery(num) {
    $battery_power_im.setAttribute('width', num * 1.9)
    $battery_power_num.textContent = num + "%"
}

function update_temp(num, temp_id) {
    let $temperature = $thermometers[temp_id - 1].getElementsByTagName("div")[0]
    $temperature.style.height = (num - config.minTemp) / (config.maxTemp - config.minTemp) * 100 + "%";
    $temperature.dataset.value = num + "°C";
}

function update_on_off(isOn, send) {
    let isButtonActive = $button.classList.contains('active')
    if (send) {
        $.ajax({
            type: "POST",
            url: "/api/changeState/isOn",
            data: {"newState": +!isButtonActive},
            success: function (msg) {
                $button.classList.toggle('active');
            }
        });
    } else {
        if ((!isButtonActive && isOn) || (isButtonActive && !isOn))
            $button.classList.toggle('active');
    }
}


function update_all_elements(parameters) {
    $.ajax({
        type: "GET",
        url: "/api/getAllData",
        dataType: "json",
        success: function (data) {
            update_battery(data["BATTERY"])
            update_temp(data["TEMP_1"], 1)
            update_temp(data["TEMP_2"], 2)
            update_temp(data["TEMP_3"], 3)
            update_on_off(data["IS_ON"], false)
        }
    });
}

$(document).ready(function () {
    $("#button-on-off").click(function () {
        update_on_off($(this), true);
    });
});

update_all_elements()
setInterval(update_all_elements, 1000);
