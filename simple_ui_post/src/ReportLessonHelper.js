import classes from "./ReportLesson.module.css";

function ReportLessonHelper(props){
    let lessons = props.data;
    let rowsForTable = [];
    let newRow = [];
    for(let i=0; i<lessons.length; i++){
        if(i%5 === 0){
            newRow = [];
        }
        let childtable = [];
        for(let j=0; j<lessons[i].length; j++){
            let lesson = lessons[i][j];
            let startTime, endTime, occurringTime, dayInWeek;

            switch(lesson["day"]){
                case 0: dayInWeek="Sunday"; break;
                case 1: dayInWeek="Monday"; break;
                case 2: dayInWeek="Tuesday"; break;
                case 3: dayInWeek="Wednesday"; break;
                case 4: dayInWeek="Thursday"; break;
                case 5: dayInWeek="Friday"; break;
                case 6: dayInWeek="Saturday"; break;
            }
            
            startTime = lesson["startTime"]["hours"].toString() + ":";
            if(lesson["startTime"]["minutes"] === 0){
                startTime += "00"
            }
            else {
                startTime += lesson["startTime"]["minutes"].toString();
            }

            endTime = lesson["endTime"]["hours"].toString() + ":";
            if(lesson["endTime"]["minutes"] === 0){
                endTime += "00"
            }
            else {
                endTime += lesson["endTime"]["minutes"].toString();
            }

            occurringTime = startTime + " to " + endTime;

            let item = [];
            item.push(<strong key="subject">{lesson["subjectName"]}</strong>);
            item.push(<br key={"s"}></br>);
            item.push(<strong key="topic">{lesson["topic"]}</strong>);
            item.push(<br key={"t"}></br>);
            item.push(<strong key="time">{occurringTime}</strong>);
            item.push(<br key={"da"}></br>);
            item.push(<strong key="day">{dayInWeek}</strong>);
            item.push(<br key={"d"}></br>);
            item.push(<strong key="date">{lesson["dateCode"]}</strong>);
            if(lesson["teachersNames"].length > 0){
                item.push(<br key={"te"}></br>);
                item.push(<strong key="teacher">Teachers:</strong>);
                item.push(<br key={"tes"}></br>);
                item.push(lesson["teachersNames"][0]);
                for (let k=1; k<lesson["teachersNames"].length; k++){
                    item.push(", ");
                    item.push(lesson["teachersNames"][k]);
                }
            }
            if(lesson["groupsNames"].length > 0){
                item.push(<br key={"gr"}></br>);
                item.push(<strong key="group">Groups:</strong>);
                item.push(<br key={"grs"}></br>);
                item.push(lesson["groupsNames"][0]);
                for (let k=1; k<lesson["groupsNames"].length; k++){
                    item.push(", ");
                    item.push(lesson["groupsNames"][k]);
                }
            }

            item.push(<br key={"cl"}></br>);
            item.push(<strong key="classroom">Classroom:</strong>);
            item.push(<br key={"cls"}></br>);
            item.push(lesson["classroomsNames"]);
            childtable.push(<tr key={j}><td key={j}>{item}</td></tr>);
        }
        if(lessons[i].length === 0){
            childtable = (<table className={classes.noData}></table>);
        }
        else{
            childtable = (<table className={classes.smallTable}><tbody>{childtable}</tbody></table>);
        }
        if(i%2 === 0){
            newRow.push(<td key={i} className={classes.even}>{childtable}</td>); 
        }   
        else{
            newRow.push(<td key={i} className={classes.odd}>{childtable}</td>); 
        }       
        if(i%5 === 4 || i === lessons.length-1){
            rowsForTable.push(<tr key={(i-i%5)/5} >{newRow}</tr>);
        }  
    }
    let result = (<table className={classes.mainTable}><tbody>{rowsForTable}</tbody></table>);      
    return result;
}

export default ReportLessonHelper;