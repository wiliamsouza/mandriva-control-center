//import Qt 4.7
import QtQuick 1.0
import "colibri"

Rectangle {
    id: main
    width: 640
    height: 480
    color: "#4d4d4d"

    Rectangle {
        id: header
        width: main.width
        height: 100
        color: "red"
    }

    Rectangle {
        id: leftServices
        y: header.height
        width: 240
        height: main.height - header.height
        color: "lightgrey"
        clip: true
        ServicesListView {
            //id: units_list_l
        }
    }

    Rectangle {
        id: right
        x: leftServices.width
        y: header.height
        width: main.width - leftServices.width
        height: main.height - header.height
        clip: true
        color: "black"
        Grid {
            id: details_grid
            columns: 2
            spacing: 6
            anchors.left: parent.left
            anchors.leftMargin: 12
            anchors.top: parent.top
            anchors.topMargin: 12
            
            Text {
                text: "Id:"
                color: "black"
                opacity: 0.6
                font.bold: true
            }
            Text {
                id: id
                //width: 200
                //elide: Text.ElideRight
                text: "N/A"
                color: "black"
                opacity: 0.6
            }

            Text {
                text: "Load State:"
                color: "black"
                opacity: 0.6
                font.bold: true
            }
            Text {
                id: load_state
                //width: 200
                //elide: Text.ElideRight
                text: "N/A"
                color: "black"
                opacity: 0.6
            }

            Text {
                text: "Active State:"
                color: "black"
                opacity: 0.6
                font.bold: true
            }
            Text {
                id: active_state
                //width: 200
                //elide: Text.ElideRight
                text: "N/A"
                color: "black"
                opacity: 0.6
            }

            Text {
                text: "Sub State:"
                color: "black"
                opacity: 0.6
                font.bold: true
            }
            Text {
                id: sub_state
                //width: 200
                //elide: Text.ElideRight
                text: "N/A"
                color: "black"
                opacity: 0.6
            }
            Row {
                id: buttons
                visible: false
                spacing: 6
                CLButton {
                    text: "Start"
                    onClicked: { serviceController.start_service(id) }
                }
                CLButton {
                    text: "Stop"
                    onClicked: { serviceController.stop_service(id) }
                }
                CLButton {
                    text: "Restart"
                    onClicked: { serviceController.restart_service(id) }
                }
            }
        }
    }
}
