import { useEffect, useState } from 'react';
import api from './api';

function App() {

    const [message, setMessage] = useState('');
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);

    // Get API root message
    useEffect(() => {

        const getApiMessage = async () => {

            try {
                const response = await api.get('/');
                setMessage(response.data.message);

            } catch (error) {
                console.error('Error connecting to API:', error);
                setMessage('Unable to connect to API');
            }
        };

        getApiMessage();

    }, []);


    // Try dummy data
    const tryDummyData = async () => {

        setLoading(true);

        try {

            // Load dummy data
            const dummyResponse = await fetch('/dummy_data.json');
            const dummyData = await dummyResponse.json();

            console.log('Dummy data:', dummyData);

            // Send data to FastAPI
            const response = await api.post(
                '/predict',
                dummyData
            );

            setPrediction(
                Math.round(response.data['Post-stroke Survival (days)'])
            );

        } catch (error) {

            console.error('Prediction error:', error);
            console.error(
                'API response:',
                error.response?.data
            );

            setPrediction('Error obtaining prediction');

        }

        setLoading(false);
    };


    return (
        <div
            style={{
                maxWidth: '800px',
                margin: '50px auto',
                fontFamily: 'Arial',
                textAlign: 'center'
            }}
        >

            <h1>{message}</h1>

            <hr />

            <h2>Post-stroke Survival Prediction</h2>

            <div
                style={{
                    fontSize: '32px',
                    margin: '30px'
                }}
            >
                {prediction !== null
                    ? `${prediction} days`
                    : 'No prediction yet'}
            </div>

            <button
                onClick={tryDummyData}
                disabled={loading}
            >
                {loading
                    ? 'Predicting...'
                    : 'Try with dummy data'}
            </button>

        </div>
    );
}

export default App;