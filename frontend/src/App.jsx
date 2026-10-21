import { useEffect, useState } from 'react';
import api from './api';
import './App.css';
import Plot from "react-plotly.js";

function App() {

    const [message, setMessage] = useState('');
    const [trialInfo, setTrialInfo] = useState(null);
    const [prediction, setPrediction] = useState(null);
    const [predictionTreat, setPredictionTreat] = useState(null);
    const [loading, setLoading] = useState(false);

    // ------------------------------------------
    // Load API information and clinical trial
    // ------------------------------------------

    useEffect(() => {

        api.get("/")
            .then(response => {
                setMessage(response.data.message);
            })
            .catch(error => {
                console.error("API connection error:", error);
            });

        api.get("/trial-info")
            .then(response => {
                console.log("Clinical trial data:", response.data);
                setTrialInfo(response.data);
            })
            .catch(error => {
                console.error("Clinical trial fetch error:", error);
            });
    }, []);


    // ------------------------------------------
    // Try model using dummy data
    // ------------------------------------------

    const tryDummyData = async () => {

        setLoading(true);

        try {

            // Load dummy data
            const dummyResponse = await fetch(
                `${import.meta.env.BASE_URL}dummy_data.json`
            );

            const dummyData = await dummyResponse.json();
            

            // Send dummy data with treatment to model
            dummyData.itt_treat = 0.0;
            const responseTreat = await api.post(
                '/predict',
                dummyData
            );

            setPredictionTreat(
                responseTreat.data[
                    'Post-stroke Survival (days)'
                ]
            );

            // Send dummy data without treatment to model
            dummyData.itt_treat = 1.0;
            const response = await api.post(
                '/predict',
                dummyData
            );

            setPrediction(
                response.data[
                    'Post-stroke Survival (days)'
                ]
            );


        } catch (error) {

            console.error(
                'Prediction error:',
                error
            );

        } finally {

            setLoading(false);

        }
    };


    return (
        <div className="dashboard">

            {(
                <section className="dataset-card">

                    <h1 href="https://datashare.ed.ac.uk/items/95f369ad-17a3-4032-b5ee-2f10b6fd724d">
                        The Third International Stroke Trial (IST-3)
                    </h1>                    
                    <a href="https://datashare.ed.ac.uk/items/95f369ad-17a3-4032-b5ee-2f10b6fd724d">
                        Source
                    </a> 
                    <h2>
                        Objective
                    </h2>
                    <p>
                        Assess impact of t-PA on stroke patients.
                    </p>
                    <h2>
                        About Dataset 
                    </h2>
                    <p>
                        Stroke patients are enrolled in treatment and control groups of the clinical trial. 
                        Their individual progress is tracked over 18 months, including 3 and 6 month intervals, monitoring their vitals and status periodically. 
                        Selected co-morbidities (eg: diabetes) and imaging are also recorded to further augment the dataset.
                    </p>
                    <h4>
                        Citation: Sandercock, P; Wardlaw, J; Lindley, R; Cohen, G; Whiteley, W. (2016). The third International Stroke Trial (IST-3), 2000-2015 [dataset]. University of Edinburgh & Edinburgh Clinical Trials Unit. https://doi.org/10.7488/ds/1350
                    </h4>                 

                </section>
            )}

            <div className="dashboard-row">

                {/* Clinical Trial Information */}

                {trialInfo && (
                    <section className="trial-grid">
                        <div className="trial-card">
                            <strong>Patients Enrolled</strong>
                            <p>
                                {trialInfo.patient_count}
                            </p>
                        </div>

                        <div className="trial-card">
                            <strong>Hospital Count</strong>
                            <p>
                                {trialInfo.hospital_count}
                            </p>
                        </div>

                        <div className="trial-card">
                            <strong>Countries Enrolled</strong>
                            <p>
                                {trialInfo.country_count}
                            </p>
                        </div>
                    </section>
                    )}

                

                {/* -------------------------------- */}
                {/* Survival Distribution Histogram */}
                {/* -------------------------------- */}

                {trialInfo && trialInfo.ages && (
                    <section className="histogram-card">
                        <Plot
                            data={[
                                {
                                    x: trialInfo.ages,
                                    type: "histogram",
                                    nbinsx: 10,
                                    hovertemplate:
                                        "Age: %{x}<br>" +
                                        "Patients: %{y}<extra></extra>",
                                    marker: {
                                        color: "#057a89",
                                        
                                    },
                                }
                            ]}
                            
                            layout={{
                                title: {
                                    text: "Ages of Enrolled Patients",
                                    font: {
                                        color: "#000000",
                                        weight: "bold",
                                        family: "Arial, sans-serif"

                                    }
                                },

                                xaxis: {
                                    title: {
                                        text: "Age",
                                        font: {
                                            color: "#000000",
                                            size: 14,
                                            weight: 100,                                        
                                            family: "Arial, sans-serif"                                         
                                        },
                                        standoff: 10
                                    },
                                    showticklabels: true,
                                    tickfont: {
                                        color: "#000000"
                                    },
                                    automargin: true
                                },

                                yaxis: {
                                    title: {
                                        text: "Number of Patients",
                                        font: {
                                            color: "#000000",
                                            size: 14,                                        
                                            family: "Arial, sans-serif"    
                                        },
                                        standoff: 20
                                    },
                                    showticklabels: true,
                                    tickfont: {
                                        color: "#000000"
                                    },
                                    automargin: true
                                },

                                bargap: 0.05,

                                margin: {
                                    l: 90,
                                    r: 30,
                                    t: 60,
                                    b: 80
                                },

                                autosize: true,
                                paper_bgcolor: "#ffffff",
                                plot_bgcolor: "#ffffff"
                            }}

                        />

                    </section>
                )}

            </div>

            {/* -------------------------------- */}
            {/* Prediction */}
            {/* -------------------------------- */}

            <section className="prediction-card">

                <h3>
                    Post-Stroke Survival Digital Twin
                </h3>

                <p>Placebo:</p>

                <div>
                    {prediction !== null
                        ? `${prediction} days`
                        : "No prediction yet"}
                </div>
                <p>Treatment:</p>

                <div>
                    {predictionTreat !== null
                        ? `${predictionTreat} days`
                        : "No prediction yet"}
                </div>

                <p></p>

                <button
                    onClick={tryDummyData}
                    disabled={loading}
                >
                    {loading
                        ? 'Predicting...'
                        : 'Try with dummy data'}
                </button>

            </section>




        </div>
    );
}

export default App;