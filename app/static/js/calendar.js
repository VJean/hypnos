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
        let prevMonthDayBtn = createDayButton(year, month - 1, daysInPrevMonth - firstDay + 1 + i);
        prevMonthDay.appendChild(prevMonthDayBtn);
        calendarDates.appendChild(prevMonthDay);
    }
  
    // Populate the days
    for (let i = 1; i <= daysInMonth; i++) {
        let day = document.createElement('div');
        day.classList.add('calendar-date');
        dayBtn = createDayButton(year, month, i);
        day.appendChild(dayBtn);
        calendarDates.appendChild(day);
    }

    // Get the last day of the month
    const lastDay = new Date(year, month + 1, 0).getDay();

    // Create blanks for days of the week after the last day
    for (let i = 1; i < 7 - lastDay; i++) {
        let nextMonthDay = document.createElement('div');
        nextMonthDay.classList.add('calendar-date', 'next-month');
        let nextMonthDayBtn = createDayButton(year, month + 1, i);
        nextMonthDay.appendChild(nextMonthDayBtn);
        calendarDates.appendChild(nextMonthDay);
    }
}

function createDayButton(year, month, day) {
    let dayBtn = document.createElement('a');
    dayBtn.classList.add('btn', 'btn-primary', 'date-item');
    // month is zero-indexed
    let night_id = `${year}${String(month+1).padStart(2, '0')}${String(day).padStart(2, '0')}`;
    dayBtn.setAttribute('href', `${SCRIPT_ROOT}/nights/${night_id}`);
    if (year == currentYear && month == currentMonth && day == currentDate.getDate()) {
        dayBtn.classList.add('date-today');
    }
    dayBtn.textContent = day;
    return dayBtn;
}

prevMonthBtn.addEventListener('click', () => {
    currentMonth--;
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    renderCalendar(currentMonth, currentYear);
});

nextMonthBtn.addEventListener('click', () => {
    currentMonth++;
    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    renderCalendar(currentMonth, currentYear);
});


renderCalendar(currentMonth, currentYear);