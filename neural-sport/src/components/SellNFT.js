import React from 'react';

function SellNFT() {
  return (
    <div className="sell-nft">
      <div className="item">
        <div className="header">
          <i className='bx bx-baseball'></i>
          <h5>The Goal!</h5>
        </div>
        <p>Neural Sport is a platform that allows users to make informed decisions about sports using AI.</p>
      </div>
      <div className="item">
        <div className="header">
          <i className='bx bx-ball'></i>
          <h5>The Execution!</h5>
        </div>
        <p>We have used a Neural Network to predict the outcome of a game. Best part we support 2 sports currently!</p>
      </div>
      <div className="item">
        <div className="header">
          <i className='bx bx-basketball'></i>
          <h5>The Future!</h5>
        </div>
        <p>If you are interested in contributing to the project, please contact us.</p>
      </div>
    </div>
  );
}

export default SellNFT;