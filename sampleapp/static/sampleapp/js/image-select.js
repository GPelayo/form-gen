$(document).ready(function () {
            window.img_slctr = $('#img_prvw').imgAreaSelect({
                instance: true,
                handles: true,
                onSelectChange: setPointFields,
                onSelectStart: setPointFields
            });
        });

function setPointFields(tag, box_data) {
    $('#id_top_left_x').val(box_data.x1);
    $('#id_top_left_y').val(box_data.y1);
    $('#id_bottom_right_x').val(box_data.x2);
    $('#id_bottom_right_y').val(box_data.y2);
};