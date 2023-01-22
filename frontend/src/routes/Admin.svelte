<main>
  <h2>Statistics</h2>
  <p>100/3000 Capybaras remaining</p>

  <h2 style="margin-top: 1em;">My recent approvals</h2>
  <div class="to-approve">
    <img src="https://capy.life/api/capy/C1JnUlnM8y-NXmroj-cz8" />
    <div class="stats">
      <h3>Name</h3>
      <p>Greg</p>

      <button class="deny">Delete</button>
    </div>
  </div>

  <h2 style="margin-top: 3em;">To approve</h2>
  <div class="to-approve">
    <img src="https://capy.life/api/capy/C1JnUlnM8y-NXmroj-cz8" />
    <div class="stats">
      <h3>Name</h3>
      <p>Greg</p>

      <button>Approve</button>
      <button>Approve with random name</button>
      <button class="deny">Deny</button>
    </div>
  </div>
</main>

<style>
  .to-approve {
    display: flex;
    margin-top: 1em;
  }

  .to-approve img {
    width: 200px;
  }

  .to-approve .stats {
    margin-left: 1em;
  }

  .to-approve button {
    margin-top: 1em;
  }

  .to-approve .deny {
    background-color: rgb(129, 26, 26);
    border: none;
  }

  .to-approve .deny:hover {
    background-color: rgb(168, 25, 25);
  }
</style>
