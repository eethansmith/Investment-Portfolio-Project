import React from 'react';

function TimeFrameFlip({ onTimeFrameChange, currentTimeFrame }) {
    return (
      <div className="time-frame-flipper">
        <button className={`time-frame-btn ${currentTimeFrame === 'All' ? 'active' : ''}`} onClick={() => onTimeFrameChange('All')}>
          All
        </button>
        <button className={`time-frame-btn ${currentTimeFrame === '1 month' ? 'active' : ''}`} onClick={() => onTimeFrameChange('1 month')}>
          Month
        </button>
        <button className={`time-frame-btn ${currentTimeFrame === '1 day' ? 'active' : ''}`} onClick={() => onTimeFrameChange('1 day')}>
          Day
        </button>
      </div>
    );
  }

  export default TimeFrameFlip;
  