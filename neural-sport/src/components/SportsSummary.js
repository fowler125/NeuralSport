import React from 'react';
import { useNavigate } from 'react-router-dom';

function SportsSummary() {
  const navigate = useNavigate();

  const handleProfileClick = (playerName) => {
    navigate(`/player/${encodeURIComponent(playerName)}`);
  };

  return (
    <div className="sports-summary">
      <div className="category">
        <a href="strikeouts/strikeouts.html">K's</a>
        <a href="playground/playground.html">Playground</a>
      </div>
      <div className="players">
        <div className="item">
          <img src="assets/Tarik Skubal.png" alt="Tarik Skubal" />
          <div className="info">
            <div>
              <h5>Tarik Skubal</h5>
              <div className="btc">
                <i className='bx bx-baseball'></i>
                <p>228 K's</p>
              </div>
            </div>
            <p>1 of 853</p>
          </div>
          <div className="bid">
            <p>Detroit Tigers</p>
            <a href="#" onClick={() => handleProfileClick('Tarik Skubal')}>Profile</a>
          </div>
        </div>
        <div className="item">
          <img src="assets/chris sale.png" alt="Chris Sale" />
          <div className="info">
            <div>
              <h5>Chris Sale</h5>
              <div className="btc">
                <i className='bx bx-baseball'></i>
                <p>225 K's</p>
              </div>
            </div>
            <p>2 of 853</p>
          </div>
          <div className="bid">
            <p>Atlanta Braves</p>
            <a href="#" onClick={() => handleProfileClick('Chris Sale')}>Profile</a>
          </div>
        </div>
        <div className="item">
          <img src="assets/Dylan Cease.png" alt="Dylan Cease" />
          <div className="info">
            <div>
              <h5>Dylan Cease</h5>
              <div className="btc">
                <i className='bx bx-baseball'></i>
                <p>224 K's</p>
              </div>
            </div>
            <p>3 of 853</p>
          </div>
          <div className="bid">
            <p>San Diego Padres</p>
            <a href="#" onClick={() => handleProfileClick('Dylan Cease')}>Profile</a>
          </div>
        </div>
        <div className="item">
          <img src="assets/Zack Wheeler.png" alt="Zack Wheeler" />
          <div className="info">
            <div>
              <h5>Zack Wheeler</h5>
              <div className="btc">
                <i className='bx bx-baseball'></i>
                <p>224 K's</p>
              </div>
            </div>
            <p>4 of 853</p>
          </div>
          <div className="bid">
            <p>Philadelphia Phillies</p>
            <a href="#" onClick={() => handleProfileClick('Zack Wheeler')}>Profile</a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SportsSummary;