<template>
  <div class="about">
    <h1>About This Boilerplate</h1>
    <div class="about-content">
      <p>
        This is a Progressive Web App (PWA) boilerplate built with Vue 3 and TypeScript for the
        frontend, and Python Flask for the backend. It provides the following features:
      </p>

      <ul>
        <li>Vue 3 Composition API with TypeScript</li>
        <li>Pinia for state management</li>
        <li>RESTful API with Flask</li>
        <li>PWA capabilities including offline support</li>
        <li>Responsive design</li>
      </ul>

      <h2>Project Structure</h2>
      <p>
        The project is organized into frontend and backend directories, making it easy to develop
        and deploy each part independently.
      </p>

      <h2>Getting Started</h2>
      <p>
        To add your own components and functionality, modify the components in the
        <code>src/components</code> directory and create new routes in <code>src/router</code>.
        Backend API endpoints can be added to <code>backend/app.py</code>.
      </p>
    </div>
  </div>
</template>

<style>
.about {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
  text-align: center;
}

.about-content {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

h2 {
  margin-top: 20px;
  margin-bottom: 10px;
  color: #343a40;
}

p {
  margin-bottom: 16px;
  line-height: 1.6;
}

ul {
  margin-bottom: 20px;
  padding-left: 20px;
}

li {
  margin-bottom: 8px;
}

code {
  background-color: #e9ecef;
  padding: 2px 4px;
  border-radius: 4px;
  font-family: monospace;
}
</style>
