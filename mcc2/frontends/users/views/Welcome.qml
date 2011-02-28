//import Qt 4.7
import QtQuick 1.0
//import Qt.labs.Mx 1.0

// ** Not used variable scope problem **

Grid {
    //anchors.centerIn: parent
    columns: 1
    rows: 2
    //anchors.centerIn: parent
    Text {
        text: "Mandriva Control Center"
        //anchors.horizontalCenter: parent.horizontalCenter
        //anchors.centerIn: parent
        font.bold: true
        font.pixelSize: 25
        color: "red"
    }
    Text {
        text: "Users and Groups"
        //anchors.horizontalCenter: parent.horizontalCenter
        //anchors.centerIn: parent
        font.bold: true
        font.pixelSize: 20
    }
}
