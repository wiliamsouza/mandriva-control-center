import QtQuick 1.0

import "/usr/share/mandriva/qt-components/desktop/components"
import "/usr/share/mandriva/qt-components/desktop/components/plugin"

Rectangle {

    SystemPalette {
        id: palette
        colorGroup: SystemPalette.Active
    }

    id: window
    width: 640
    height: 480
    color: palette.window



    Rectangle {
        id: header
        width: window.width
        height: 50
        color: palette.window

        Row {
            anchors.left: parent.left
            anchors.leftMargin: 6
            anchors.verticalCenter: parent.verticalCenter

            Button {
                text: qsTr("All")
                onClicked: {
                    controller.search(serviceModel, "")
                    servicesListView.currentIndex = 0
                }
            }

            Button {
                text: qsTr("Active")
                onClicked: {
                    controller.search(serviceModel, "^active$")
                    servicesListView.currentIndex = 0
                }
            }

            Button {
                text: qsTr("Inactive")
                    onClicked: {
                        controller.search(serviceModel, "^inactive$")
                        servicesListView.currentIndex = 0
                }
            }

            Button {
                text: qsTr("Failed")
                    onClicked: {
                        controller.search(serviceModel, "^failed$")
                        servicesListView.currentIndex = 0
                }
            }
        }

        TextField {
            id: searchField
            anchors.right: parent.right
            anchors.rightMargin: 6
            anchors.verticalCenter: parent.verticalCenter
            onTextChanged: controller.search(serviceModel, text)
        }
    }

    Rectangle {
        id: content
        y: header.height
        height: window.height - header.height
        width: window.width
        color: palette.alternateBase
        clip: true

        Component {
            id: serviceDelegate

            Item {
                id: serviceRect
                width: content.width
                height: 40

                Row {
                    id: serviceItem
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    anchors.leftMargin: 12
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

                        Text {
                            id: title
                            width: (content.width - icon.height) / 2
                            elide: Text.ElideRight
                            text: model.service.name
                            color: palette.text
                            font.bold: true
                        },

                        Text {
                            id: subtitle
                            width: (content.width - icon.height) / 2
                            elide: Text.ElideRight
                            text: model.service.description
                            color: palette.text
                        }
                    ]
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        servicesListView.currentItem.state = ""
                        servicesListView.currentIndex = index
                        servicesListView.currentItem.state = "show"
                    }
                }

                Row {
                    id: actionButtons
                    opacity: 0
                    anchors.top: parent.top
                    anchors.topMargin: 20
                    anchors.right: parent.right
                    anchors.rightMargin: 6

                    Button {
                        text: qsTr("Start")
                        onClicked: {
                            controller.start_service(serviceModel, model.service.name, index)
                        }
                    }

                    Button {
                        text: qsTr("Stop")
                        onClicked: {
                            controller.stop_service(serviceModel, model.service.name, index)
                        }
                    }

                    Button {
                        text: qsTr("Restart")
                        onClicked: {
                            controller.restart_service(serviceModel, model.service.name, index)
                        }
                    }
                }

                states : State {
                    name: "show"
                    PropertyChanges { target: actionButtons; opacity: 1}
                }

                // FIXME: only start this animation after the highlight animation.
                transitions: Transition {
                    NumberAnimation { properties: "opacity"; duration: 800 }
                }
            }
        }

        Component {
            id: highlightServices

            Rectangle {
                width: content.width
                height: 40
                color: palette.highlight
                y: servicesListView.currentItem.y;
                Behavior on y { SpringAnimation { spring: 2; damping: 0.4 } }
            }
        }

        ListView {
            id: servicesListView
            anchors.fill: parent
            model: serviceModel
            delegate: serviceDelegate
            highlight: highlightServices
            highlightFollowsCurrentItem: false
       }
    }
}
