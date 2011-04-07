//import Qt 4.7
import QtQuick 1.0

ListView {
    id: unit_list
    width: leftServices.width
    height: leftServices.height
    //anchors.fill: parent
    model: serviceModel
    delegate: Component {
        Rectangle {
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
                }
            }
        }
    }
    states: State {
        name: "ShowBars"
        when: unit_list.movingVertically
        PropertyChanges { target: verticalScrollBar; opacity: 1 }
    }
    ScrollBar {
        id: verticalScrollBar
        width: 12
        height: unit_list.height-12
        anchors.right: unit_list.right
        opacity: 0
        orientation: Qt.Vertical
        position: unit_list.visibleArea.yPosition
        pageSize: unit_list.visibleArea.heightRatio
    }
}
