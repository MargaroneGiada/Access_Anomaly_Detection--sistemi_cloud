import { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';
import './Dashboard.css';
import { useNavigate } from 'react-router-dom';


function Dashboard() {
  const hourlyChartRef = useRef(null);
  const countryChartRef = useRef(null);

  const hourlyChartInstance = useRef(null);
  const countryChartInstance = useRef(null);

  const navigate = useNavigate();

  const [tokens, setTokens] = useState(null);

  const handleEventClick = () => {
    !tokens ? navigate('/login') : navigate('/')
  }

  useEffect(() => {

    if (hourlyChartInstance.current) {
      hourlyChartInstance.current.destroy();
    }
    if (countryChartInstance.current) {
      countryChartInstance.current.destroy();
    }

    hourlyChartInstance.current = new Chart(hourlyChartRef.current, {
      type: 'line',
      data: {
        labels: Array.from({ length: 24 }, (_, i) => i.toString().padStart(1, '0')),
        datasets: [{
          label: 'Numero Accessi',
          data: [3, 2, 1, 0, 0, 2, 4, 7, 10, 12, 9, 8, 7, 9, 11, 14, 13, 9, 6, 5, 4, 3, 2, 1],
          fill: false,
          borderColor: 'rgb(189, 46, 46)',
          tension: 0.1
        }]
      },
      options: { respo16b462rrm11goc4ckidss92uqcnsive: true }
    });

    countryChartInstance.current = new Chart(countryChartRef.current, {
      type: 'pie',
      data: {
        labels: ['Italia', 'USA', 'Russia', 'India', 'Germania'],
        datasets: [{
          data: [45, 25, 10, 15, 5],
          backgroundColor: ['#007bff', '#28a745', '#dc3545', '#ffc107', '#6f42c1']
        }]
      },
      options: { responsive: true }
    });

    return () => {
      if (hourlyChartInstance.current) {
        hourlyChartInstance.current.destroy();
        hourlyChartInstance.current = null;
      }
      if (countryChartInstance.current) {
        countryChartInstance.current.destroy();
        countryChartInstance.current = null;
      }
    };
  }, []);
  
  return (
    <div className="Dashboard">
      <header>
        <h1>Dashboard</h1>
        {!tokens ? (
          <button onClick={() => handleEventClick()}>Login</button>
        ) : (
          <>
            <p>Benvenutə, ***</p>
           <button onClick={navigate('/')}>Logout</button>
        </>
)}
      </header>

      <div className="container">
        
        <div className="card col-1">
          <h2>Accessi per ora del giorno</h2>
          <canvas className='line' ref={hourlyChartRef}></canvas>
        </div>

        <div className="card col-2">
          <h2>Distribuzione IP per Paese</h2>
          <canvas className="pie" ref={countryChartRef}></canvas>
        </div>


        <div className="card col-1">
          <h2>Accessi anomali recenti</h2>
          <table>
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>IP</th>
                <th>Paese</th>
                <th>Motivo</th>
              </tr>
            </thead>
            <tbody>
              <tr><td>2025-07-01 09:21</td><td>203.0.113.42</td><td>Russia</td><td>Accesso fuori orario</td></tr>
              <tr><td>2025-07-01 02:15</td><td>198.51.100.23</td><td>USA</td><td>IP sconosciuto</td></tr>
              <tr><td>2025-06-30 23:05</td><td>102.64.22.5</td><td>India</td><td>Login falliti ripetuti</td></tr>
            </tbody>
          </table>
        </div>

        <div className="card col-2">
          <h2>Notifiche recenti</h2>
          <ul>
            <li>2025-07-01 09:21 - Anomalia da Russia</li>
            <li>2025-07-01 02:15 - Accesso da IP sconosciuto</li>
          </ul>
        </div> 
      </div>
    </div>
  );
}

export default Dashboard;