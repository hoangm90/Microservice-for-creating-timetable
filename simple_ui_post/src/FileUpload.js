import React, { useState, useCallback } from 'react';
import ReportLesson from './ReportLesson';
import classes from './FileUpload.module.css'

function FileUpload(){
    const [chosenFile, setChosenFile] = useState(null);
    const [data, setData] = useState(null);
    const [lessonColor, setLessonColor] = useState(null);
    
    const calculateTimetable = useCallback((d) => {
        if ("error" in d){
            alert(d["error"])
        }
        else {
            let lessons = d["events"];
            let colors = [];
            console.log(d);
            if(lessons.length >= 1){
                let maxDay = new Date(lessons[0]["dateCode"]);
                let minDay = new Date(lessons[0]["dateCode"]);
                for(let i=1; i <lessons.length; i++){
                    let d = new Date(lessons[i]["dateCode"]);
                    if (d > maxDay){
                        maxDay = d;
                    }
                    if (d < minDay){
                        minDay = d;
                    }
                }
                let numDay = (maxDay-minDay)/1000/3600/24 + 1;
                for(let i=0; i<numDay; i++){
                    for(let j=0; j<5; j++){
                        colors.push([]);
                    }
                }
                for(let i=0; i <lessons.length; i++){
                    let d = new Date(lessons[i]["dateCode"])
                    let color = ((d-minDay)/1000/3600/24)*5;
                    switch(lessons[i]["startTime"]["hours"]){
                        case 8: break;
                        case 9: color += 1; break;
                        case 11: color += 2; break;
                        case 14: color += 3; break;
                        case 16: color += 4; break;
                    }
                    lessons[i]["day"] = d.getDay();
                    colors[color].push(lessons[i]) ;
                }
            }
            setLessonColor(colors);
            setData(d);
        }        
    }, []);

    const changeHandler = (event) => {
        setChosenFile(event.target.files[0])
    }
    const handleSubmit = (event) => {
        if(!chosenFile) {
            alert("No file chosen!");
            return ;
        }
        setData("");
        const reader = new FileReader();
        reader.readAsText(chosenFile); //async function
        reader.onload = function(event){
            fetch("http://127.0.0.1:5003/api/makeplan",
            {
                method: "POST",
                body: reader.result,
            }
            ).then(r => r.json())
            .then(d => calculateTimetable(d))
        }
        
    }

    if(data === ""){
        return (
            <div className={classes.main}>
            <input type="file" name="file" onChange={changeHandler}/>
            <br/>
            <br/>
            <button onClick={handleSubmit}>Send file</button>
            <br/>
            <br/>
            <h1>Wait For A Moment!</h1>
        </div>
        )
    }

    return (
        <>
        <div className={classes.main}>
            <input type="file" name="file" onChange={changeHandler}/>
            <br/>
            <br/>
            <button onClick={handleSubmit}>Send file</button>
            <br/>
            <br/>
        </div>
        {
            data &&
            <ReportLesson lessons={lessonColor} teachers={data["teachers"]} groups={data["groups"]} classrooms={data["classrooms"]} />
        }
        
        </>
        
    )
}
export default FileUpload;