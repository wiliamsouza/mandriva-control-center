//import Qt 4.7
import QtQuick 1.0

// ** Not used variable scope problem **

Component {
    //id: listViewHighlight
    Rectangle {
        color: "lightsteelblue"
        radius: 8
        y: listView.currentItem.y
        Behavior on y {
            SpringAnimation {
                spring: 3
                damping: 0.2
            }
        }
    }
}
