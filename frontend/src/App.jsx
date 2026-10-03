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
                setApiStatus(response.data.message);
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
                '/dummy_data.json'
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
                <section className="intro-card">

                    <strong>
                        The Third International Stroke Trial (IST-3)
                    </strong>                    

                </section>
            )}

            <div className="dashboard-row">

                {/* -------------------------------- */}
                {/* Clinical Trial Information */}
                {/* -------------------------------- */}

                {trialInfo && (
                    <section className="trial-grid">
                        <div className="trial-card">
                            <strong>Enrolled Patient Count</strong>
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

                        <h2>
                            Ages of Enrolled Patients
                        </h2>

                        <Plot
                            data={[
                                {
                                    x: trialInfo.ages,
                                    type: "histogram",
                                    nbinsx: 10,
                                    hovertemplate:
                                        "Age: %{x}<br>" +
                                        "Patients: %{y}<extra></extra>"
                                }
                            ]}
                            layout={{
                                xaxis: {
                                    title: "Age"
                                },

                                yaxis: {
                                    title: "Number of Patients"
                                },

                                bargap: 0.05,

                                margin: {
                                    l: 70,
                                    r: 30,
                                    t: 30,
                                    b: 70
                                },

                                autosize: true
                            }}
                            useResizeHandler={true}
                            style={{
                                width: "100%",
                                height: "400px"
                            }}
                            config={{
                                responsive: true,
                                displayModeBar: false
                            }}
                        />

                    </section>
                )}

            </div>

            {/* -------------------------------- */}
            {/* Prediction */}
            {/* -------------------------------- */}

            <section className="prediction-card">

                <h2>
                    Post-Stroke Survival Digital Twin
                </h2>

                <div>
                    {prediction !== null
                        ? `Placebo: ${prediction} days`
                        : "Placebo: No prediction yet"}
                </div>

                <div>
                    {predictionTreat !== null
                        ? `Treatment: ${predictionTreat} days`
                        : "Treatment: No prediction yet"}
                </div>

                <button
                    onClick={tryDummyData}
                    disabled={loading}
                >
                    {loading
                        ? 'Predicting...'
                        : 'Try with dummy data'}
                </button>

            </section>

            {(
                <section className="outro-card">
                    <strong>About Dataset</strong>
                    <p>
                        Source: https://datashare.ed.ac.uk/items/95f369ad-17a3-4032-b5ee-2f10b6fd724d
                    </p>
                    <p>
                        Citation: Sandercock, P; Wardlaw, J; Lindley, R; Cohen, G; Whiteley, W. (2016). The third International Stroke Trial (IST-3), 2000-2015 [dataset]. University of Edinburgh & Edinburgh Clinical Trials Unit. https://doi.org/10.7488/ds/1350
                    </p>                  

                </section>
            )}


        </div>
    );
}

export default App;