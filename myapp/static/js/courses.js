function showSection(id) {
    const sections = document.querySelectorAll('.course-section');
    sections.forEach(sec => sec.classList.remove('active'));

    const buttons = document.querySelectorAll('.sidebar1 button');
    buttons.forEach(btn => btn.classList.remove('active'));

    document.getElementById(id).classList.add('active');
    const index = ['scratch', 'python', 'ml', 'web', 'app'].indexOf(id);
    if (index !== -1) buttons[index].classList.add('active');
  }