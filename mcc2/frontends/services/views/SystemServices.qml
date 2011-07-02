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
                height: 27
                onClicked: {
                    controller.search(serviceModel, "")
                    servicesListView.currentIndex = 0
                }
            }

            Button {
                text: qsTr("Active")
                height: 27
                onClicked: {
                    controller.search(serviceModel, "^active$")
                    servicesListView.currentIndex = 0
                }
            }

            Button {
                text: qsTr("Inactive")
                height: 27
                onClicked: {
                    controller.search(serviceModel, "^inactive$")
                    servicesListView.currentIndex = 0
                }
            }

            Button {
                text: qsTr("Failed")
                height: 27
                onClicked: {
                    controller.search(serviceModel, "^failed$")
                    servicesListView.currentIndex = 0
                }
            }
        }

        TextField {
            id: searchField
            height: 27
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
                width: content.width - vscrollbar.width
                height: 40

                Row {
                    id: serviceItem
                    spacing: 0
                    children: [

                        Item {
                            id: icon
                            width: 50
                            height: serviceRect.height

                            Image {
                                width: 16
                                height: 16
                                source: "images/" + model.service.activeState + ".png"
                                anchors.centerIn: parent
                            }
                        },

                        Text {
                            id: title
                            width: ((content.width - icon.width) - vscrollbar.width) / 2
                            elide: Text.ElideRight
                            text: model.service.name
                            color: palette.text
                            font.bold: true
                            anchors.verticalCenter: parent.verticalCenter
                        },

                        Text {
                            id: subtitle
                            width: ((content.width - icon.width) - vscrollbar.width) / 2
                            elide: Text.ElideRight
                            text: model.service.description
                            color: palette.text
                            anchors.verticalCenter: parent.verticalCenter
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
                width: content.width - vscrollbar.width
                height: 40
                color: palette.highlight
                y: servicesListView.currentItem.y;
                Behavior on y { SpringAnimation { spring: 2; damping: 0.4 } }
            }
        }

        Component {
            id: headerDelegate

            Row {
                id: headerRow
                spacing: 0
                property int headerHeight: 30
                property int headerMinWidth: 50
                children: [

                    QStyleItem {
                        elementType: "header"
                        raised: true
                        width: headerMinWidth
                        height: headerHeight
                        text: qsTr("Status")
                    },

                    QStyleItem {
                        elementType: "header"
                        raised: true
                        width: ((content.width - headerMinWidth) - vscrollbar.width) / 2
                        height: headerHeight
                        text: qsTr("Service")
                    },

                    QStyleItem {
                        elementType: "header"
                        raised: true
                        width: ((content.width - headerMinWidth) - vscrollbar.width)/ 2
                        height: headerHeight
                        text: qsTr("Description")
                    }
                ]
            }
        }

        ListView {
            id: servicesListView
            anchors.fill: parent
            model: serviceModel
            delegate: serviceDelegate
            header: headerDelegate
            highlight: highlightServices
            highlightFollowsCurrentItem: false
            focus: true
            onContentYChanged:  {
                vscrollbar.value = servicesListView.contentY
            }
        }

        ScrollBar {
            id: vscrollbar
            property int availableHeight : content.height - 30
            orientation: Qt.Vertical
            maximumValue: servicesListView.contentHeight > availableHeight ? servicesListView.contentHeight - availableHeight : 0
            minimumValue: 0
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            onValueChanged: {
                servicesListView.contentY = value
            }
        }
    }
}
