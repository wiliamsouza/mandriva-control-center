//import Qt 4.7
import QtQuick 1.0
//import "colibri"

import "components"
import "components/plugin"

Rectangle {
    id: main
    width: 640
    height: 480
    color: "#4d4d4d"

    Rectangle {
        id: header
        width: main.width
        height: 100
        color: "#333333"

        Image {
            id: mandrivaLogo
            source: "images/mandriva_logo.png"
            anchors.left: parent.left
            anchors.leftMargin: 12
            anchors.verticalCenter: parent.verticalCenter
        }
    }

    Rectangle {
        id: leftServices
        y: header.height
        width: 240
        height: main.height - header.height
        color: "lightgrey"
        clip: true



        ListView {
            id: unit_list
            width: leftServices.width
            height: leftServices.height
            //anchors.fill: parent
            model: serviceModel
            delegate: Component {
                Rectangle {
                    id: myRec
                    width: unit_list.width
                    height: 40
                    color: ((index % 2 == 0) ? "#b3b3b3" : "#808080")
                    Row {
                        anchors.verticalCenter: parent.verticalCenter
                        spacing: 12
                        children: [
                            Image {
                                id: icon
                                width: 16
                                height: 16
                                source: "images/green.png"
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.leftMargin: 4
                            },
                            Column {
                                anchors.verticalCenter: parent.verticalCenter
                                children: [
                                    Text {
                                        id: title
                                        width: 200
                                        elide: Text.ElideRight
                                        text: model.service.name
                                        //color: "black"
                                        opacity: 0.7
                                        font.bold: true
                                        //anchors.left: parent.left
                                        //anchors.leftMargin: 4
                                    },
                                    Text {
                                        id: subtitle
                                        width: 200
                                        elide: Text.ElideRight
                                        text: model.service.description
                                        opacity: 0.7
                                        //color: "grey"
                                        //anchors.left: parent.left
                                        //anchors.leftMargin: 4
                                    }
                                ]
                            }
                        ]
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            unit_list.currentIndex = index
                            description.text = model.service.description
                            id.text = model.service.name
                            load_state.text = model.service.load_state
                            active_state.text = model.service.active_state
                            sub_state.text = model.service.sub_state
                            serviceController.service_selected(model.service)
                            details_grid.visible = true
                            buttons.visible = true
                            myRec.height = 100
                        }
                    }
                }
            }

            states: State {
                name: "ShowBars"
                when: unit_list.movingVertically
                PropertyChanges { target: verticalScrollBar; opacity: 1}
            }

            ScrollBar {
                id: verticalScrollBar
                width: 12
                height: unit_list.height-12
                anchors.right: unit_list.right
                opacity: 0
                orientation: Qt.Vertical
                //position: unit_list.visibleArea.yPosition
                //pageSize: unit_list.visibleArea.heightRatio
            }
        }
    }

    Rectangle {
        id: right
        x: leftServices.width
        y: header.height
        width: main.width - leftServices.width
        height: main.height - header.height
        clip: true
        color: "#4d4d4d"

        Grid {
            id: details_grid
            visible: false
            columns: 2
            spacing: 6
            anchors.left: parent.left
            anchors.leftMargin: 12
            anchors.top: parent.top
            anchors.topMargin: 12

            Text {
                text: "Description:"
                color: "black"
                opacity: 0.6
                font.bold: true
            }
            Text {
                id: description
                width: 300
                elide: Text.ElideRight
                text: "N/A"
                color: "black"
                opacity: 0.6
            }

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
        }

        Rectangle {
            id: buttons
            visible: false
            height: 42
            width: right.width
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            color: "#333333"

            Row {
                spacing: 12
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right
                anchors.rightMargin: 6

                Button {
                    text:"Start"
                    width: 70
                    height: 30
                    onClicked: {
                        serviceController.start_service(id, unit_list.model, unit_list.currentIndex)
                    }
                }

                Button {
                    text:"Stop"
                    width: 70
                    height: 30
                    onClicked: serviceController.stop_service(unit_list.model, unit_list.currentIndex)
                }

                Button {
                    text:"Restart"
                    width: 70
                    height: 30
                    onClicked: serviceController.restart_service(id, unit_list.model, unit_list.currentIndex)
                }
            }
        }

    }
}
