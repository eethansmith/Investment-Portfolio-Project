import React from 'react';

function TimeFrameFlip({ onTimeFrameChange, currentTimeFrame }) {
    return (
      <div className="time-frame-flipper">
        <button className={`time-frame-btn ${currentTimeFrame === 'All' ? 'active' : ''}`} onClick={() => onTimeFrameChange('All')}>
          All
        </button>
        <button className={`time-frame-btn ${currentTimeFrame === 'Month' ? 'active' : ''}`} onClick={() => onTimeFrameChange('Month')}>
          Month
        </button>
        <button className={`time-frame-btn ${currentTimeFrame === 'Day' ? 'active' : ''}`} onClick={() => onTimeFrameChange('Day')}>
          Day
        </button>
      </div>
    );
  }

  export default TimeFrameFlip;
  