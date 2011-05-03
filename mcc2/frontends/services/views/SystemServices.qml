import QtQuick 1.0

import "components"
import "components/plugin"

Rectangle {
    id: window
    width: 640
    height: 480
    color: "#4d4d4d"

    Rectangle {
        id: header
        width: window.width
        height: 100
        color: "#333333"

        Image {
            id: mandrivaLogo
            source: "images/mandriva_logo.png"
            anchors.left: parent.left
            anchors.leftMargin: 12
            anchors.verticalCenter: parent.verticalCenter
        }
        /*
        TextField {
            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter
            onTextChanged: controller.search(serviceModel, text)
        }
        */
    }

    Rectangle {
        id: content
        y: header.height
        height: window.height - header.height
        width: window.width
        color: "#4d4d4d"
        clip: true


        Component {
            id: serviceDelegate

            Rectangle {
                id: serviceRect
                width: content.width
                height: 60
                color: ((index % 2 == 0) ? "#808080": "#999999")
                clip: true


                Image {
                    id: arrow
                    source: "images/arrow.png"
                    anchors.right: parent.right
                    anchors.rightMargin: 12
                    anchors.top: parent.top
                    anchors.topMargin: 12
                    smooth: true

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            serviceRect.state == "show" ? serviceRect.state = "" : serviceRect.state = "show"
                            serviceRect.state == "show" ? arrow.state = "rotated" : arrow.state = ""
                        }
                    }

                    states: State {
                        name: "rotated"
                        PropertyChanges { target: arrow; rotation: 90 }
                    }

                    transitions: Transition {
                        NumberAnimation { properties: "rotation"; duration: 500 }
                    }
                }

                Column {
                    //anchors.verticalCenter: parent.verticalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 12
                    anchors.left: parent.left
                    anchors.leftMargin: 12
                    spacing: 12

                    Row {
                        id: serviceItem

                        spacing: 12
                        children: [

                            Image {
                                id: icon
                                width: 16
                                height: 16
                                source: "images/" + model.service.activeState + ".png"
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.leftMargin: 4
                            },

                            Column {
                                anchors.verticalCenter: parent.verticalCenter
                                spacing: 6
                                children: [

                                    Text {
                                        id: title
                                        width: content.width - 80
                                        elide: Text.ElideRight
                                        text: model.service.name
                                        opacity: 0.7
                                        font.bold: true
                                    },

                                    Text {
                                        id: subtitle
                                        width: content.width
                                        elide: Text.ElideRight
                                        text: model.service.description
                                        opacity: 0.7
                                    }
                                ]
                            }
                        ]
                    }

                    Row {
                        spacing: 6
                        anchors.left: parent.left
                        anchors.leftMargin: 28

                        Text {
                            text: qsTr("Status:")
                            font.bold: true
                            opacity: 0.7
                        }

                        Text {
                           // width: content.width
                            //elide: Text.ElideRight
                            text: model.service.loadState
                            opacity: 0.7
                        }

                        Text {
                            //width: content.width
                            //elide: Text.ElideRight
                            text: model.service.activeState
                            opacity: 0.7
                        }

                        Text {
                            //width: content.width
                            //elide: Text.ElideRight
                            text: model.service.subState
                            opacity: 0.7
                        }
                    }

                    Row {
                        spacing: 12
                        anchors.right: parent.right
                        anchors.rightMargin: 50

                        Button {
                            text: qsTr("Start")
                            width: 70
                            height: 30
                            onClicked: {
                                controller.start_service(serviceModel, index)
                            }
                        }

                        Button {
                            text: qsTr("Stop")
                            width: 70
                            height: 30
                            onClicked: {
                                controller.stop_service(serviceModel, index)
                            }
                        }

                        Button {
                            text: qsTr("Restart")
                            width: 70
                            height: 30
                            onClicked: controller.restart_service(serviceModel, index)
                        }
                    }
                }

                states : State {
                    name: "show"
                    PropertyChanges { target: serviceRect; height: 130}
                }

                transitions: Transition {
                    NumberAnimation { properties: "height"; duration: 500 }
                }
            }
        }

        ListView {
            id: servicesListView
            anchors.fill: parent
            model: serviceModel
            delegate: serviceDelegate
       }
    }
}
