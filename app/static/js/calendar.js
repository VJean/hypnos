const monthYear = document.getElementById('month-year');
const calendarDates = document.querySelector('.calendar-body');
const prevMonthBtn = document.getElementById('prev-month');
const nextMonthBtn = document.getElementById('next-month');

let currentDate = new Date();
let currentMonth = currentDate.getMonth();
let currentYear = currentDate.getFullYear();

const months = [
  'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
  'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
];

function renderCalendar(month, year) {
    calendarDates.innerHTML = '';
    monthYear.textContent = `${months[month]} ${year}`;
  
    // Get the first day of the month
    const firstDay = new Date(year, month, 1).getDay();
  
    // Get the number of days in the month
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    // Get the number of days in the previous month
    const daysInPrevMonth = new Date(year, month, 0).getDate();
  
    // Create blanks for days of the week before the first day
    for (let i = 0; i < firstDay; i++) {
        let prevMonthDay = document.createElement('div');
        prevMonthDay.classList.add('calendar-date', 'prev-month');
        let prevMonthDayBtn = document.createElement('button')
        prevMonthDayBtn.classList.add('date-item');
        prevMonthDayBtn.textContent = daysInPrevMonth - firstDay + 1 + i;
        prevMonthDay.appendChild(prevMonthDayBtn);
        calendarDates.appendChild(prevMonthDay);
    }
  
    // Populate the days
    for (let i = 1; i <= daysInMonth; i++) {
        let day = document.createElement('div');
        day.classList.add('calendar-date');
        let dayBtn = document.createElement('button');
        dayBtn.classList.add('date-item');
        if (year == currentYear && month == currentMonth && i == currentDate.getDate()) {
            dayBtn.classList.add('date-today');
        }
        dayBtn.textContent = i;
        day.appendChild(dayBtn);
        calendarDates.appendChild(day);
    }

    // Get the last day of the month
    const lastDay = new Date(year, month + 1, 0).getDay();

    // Create blanks for days of the week after the last day
    for (let i = 1; i < 7 - lastDay; i++) {
        let nextMonthDay = document.createElement('div');
        nextMonthDay.classList.add('calendar-date', 'next-month');
        let nextMonthDayBtn = document.createElement('button')
        nextMonthDayBtn.classList.add('date-item');
        nextMonthDayBtn.textContent = i;
        nextMonthDay.appendChild(nextMonthDayBtn);
        calendarDates.appendChild(nextMonthDay);
    }
}

renderCalendar(currentMonth, currentYear);

// <!-- calendar previous month -->
// <div class="calendar-date prev-month">
//     <button class="date-item">26</button>
// </div>

// <!-- calendar current month -->
// <div class="calendar-date">
//     <button class="date-item">1</button>
// </div>

// <!-- calendar date: today -->
// <div class="calendar-date">
//     <button class="date-item date-today">4</button>
// </div>

// <!-- calendar date: tooltip -->
// <div class="calendar-date tooltip" data-tooltip="You have appointments">
//     <button class="date-item">5</button>
// </div>

// <!-- calendar date: not available -->
// <div class="calendar-date tooltip" data-tooltip="Not available">
//     <button class="date-item" disabled="">6</button>
// </div>

// <!-- calendar next month -->
// <div class="calendar-date next-month">
//     <button class="date-item">1</button>
// </div>