<script>
	import { onMount} from "svelte";
  let isAuthenticated = false;
	let csrfToken;
	let email;
	let password;
	let name;
	let post_data = [];
	let post_content;
	let post_title;
	let create = true;
	let message = "You have been logged in."
	let category = "success"

	let edit_post_id = 0
	let edit_post_title = ""
	let edit_post_content = ""



	onMount(async () =>  {
    fetch("http://localhost:5000/user/getsession", {
      credentials: "include",

    })
    .then((res) => res.json())
		
    .then((data) => {
      if (data.login == true) {
        isAuthenticated = true;
				getposts();
      } else {
        isAuthenticated = false;
        csrf();
      }
    })
    .catch((err) => {
      console.log(err);
    });
  });

const csrf = () => {
	fetch("http://localhost:5000/user/getcsrf", {
		credentials: "include",
	})
	.then((res) => {
		csrfToken = res.headers.get(["X-CSRFToken"])
		console.log(csrfToken)
	})
	.catch((err) => {
		console.log(err);
	});
}


const login = () => {
    fetch("http://localhost:5000/user/login", {
      method: "POST",
      headers: {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      credentials: "include",
      body: JSON.stringify({ email: email, password: password }),
    })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      if (data.login == true) {
        isAuthenticated = true;
				getposts();
      }
    })
    .catch((err) => {
      console.log(err);
    });
  }

	const getposts = () => {
    fetch("http://localhost:5000/post", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      credentials: "include",
    })
    .then((res) => res.json())
    .then((data) => {
			post_data = data
			console.log(post_data)
    })
    .catch((err) => {
      console.log(err);
    });
  };

	const createpost = () => {
		console.log(JSON.stringify({ title: post_title, content: post_content}))
		console.log()
    fetch("http://localhost:5000/post", {
      method: "POST",
      headers: {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      credentials: "include",
      body: JSON.stringify({ title: post_title, content: post_content}),
    })
    .then((res) => res.json())
    .then((data) => {
      message = "Your post has been published!"
			getposts()
			post_title = ""
			post_content = ""
    })
    .catch((err) => {
      console.log(err);
    });
  }

	const deletepost = (id) => {
    fetch("http://localhost:5000/post", {
      method: "DELETE",
      headers: {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      credentials: "include",
      body: JSON.stringify({ id:id }),
    })
    .then((res) => res.json())
    .then((data) => {
			message = "Your post has been deleted!"
			getposts()
    })
    .catch((err) => {
      console.log(err);
    });
  }

	const updatepost = (id,title,content) => {
		post_title = title
		post_content = content
    fetch("http://localhost:5000/post", {
      method: "PUT",
      headers: {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      credentials: "include",
      body: JSON.stringify({ id:id, title: post_title, content: post_content}),
    })
    .then((res) => res.json())
    .then((data) => {
			message = "Your messege has been updated!"
			getposts()
			post_title = ""
			post_content = ""
    })
    .catch((err) => {
      console.log(err);
    });
  }


  const logout = () => {
    fetch("http://localhost:5000/user/logout", {
      credentials: "include",
    })
    .then(() => {
      isAuthenticated = false;
    })
    .catch((err) => {
      console.log(err);
    });
  };


</script>

<!-- Navbar-->
<header class="site-header">
  <nav class="navbar navbar-expand-md navbar-dark bg-steel fixed-top">
    <div class="container">
      <a class="navbar-brand mr-4" href="/">Dashboard</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggle" aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarToggle">
        <div class="navbar-nav mr-auto">
        </div>
        <!-- Navbar Right Side -->
             {#if isAuthenticated}
             <div class="navbar-nav">

            <a class="nav-item nav-link" on:click={logout}>Logout</a>
            </div>

            {/if}

      </div>
    </div>
  </nav>
</header>

<main class="container">
	<div class="row">
	

	{#if isAuthenticated}
		<div class="col-md-8">
			<div class="alert alert-{category}">
				{message}
			</div>
		
		
			<!-- dashboard-->
		{#if post_data.length < 1}
			<article class="media content-section">
				<div class="media-body">
						<h1>No posts yet! Create one up above.</h1>
				</div>
			</article>

		{:else}
			{#each post_data as post }
			<article class="media content-section">
				<div class="media-body">
					<div class="article-metadata">
						<small class="text-muted">{ post.date_posted }</small>
				 		<h6 class="mr-2">{ post.author_name} ({ post.author_role })</h6>
					</div>
					<h2 class="article-title">{ post.title }</h2>
					<p class="article-content">{ post.content }</p>
					<button class="btn btn-secondary btn-sm mt-1 mb-1" on:click={() => {
						create = !create
						edit_post_id = post.id
						edit_post_title = post.title
						edit_post_content = post.content
						message = "Edit your messege before you republish it!"
						}}>
						Edit
					</button>
					<button class="btn btn-danger btn-sm mt-1 mb-1" on:click={deletepost(post.id,post.author_role)}>
						Delete
				</button>
				</div>
			</article>
			{/each}
		{/if}
		</div>
		<!-- new/edit post-->
		<div class="col-md-4">
			<div class="content-section">
			{#if create == true}
				<legend class="border-bottom mb-4">New Post</legend>
				<fieldset class="form-group">
					<div class="form-group">
						<label class="form-control-label" for="title">Title: </label>
						<input class="form-control form-control-lg" id = "title" bind:value={post_title} />
		
		
						<label class="form-control-label" for="content">Content: </label>
						<input class="form-control form-control-lg" id = "content" bind:value={post_content} />
					</div>
					<div class="form-group">
						<button class="btn btn-outline-info" on:click={createpost}>
							Publish
						</button>
					</div>
				</fieldset>
			{:else}
					<legend class="border-bottom mb-4">Edit Post</legend>
					<fieldset class="form-group">
						<div class="form-group">
							<label class="form-control-label" for="title">Title: </label>
							<input class="form-control form-control-lg" id = "title" bind:value={edit_post_title} />
							<label class="form-control-label" for="content">Content: </label>
							<input class="form-control form-control-lg" id = "content" bind:value={edit_post_content} />
						</div>
						<div class="form-group">
							<button class="btn btn-outline-info" on:click={() => {
								create = !create
								updatepost(edit_post_id,edit_post_title,edit_post_content)
								}}>Update
							</button>
						</div>
					</fieldset>
		
			{/if}
			</div>
			</div>


	<!-- when not logged in -->
	{:else}
	
		<div class="content-section">
			<div class="cover-container d-flex h-100 p-3 mx-auto flex-column">

				<main role="main" class="inner cover">
					<h1 class="cover-heading">Home Page</h1>
					<p class="lead">Please log-in with the email and password provided in user.json to test this app's functionalities.</p>
					<p class="lead">
					</p>
				</main>
			
				<footer class="mastfoot mt-auto">
					<div class="inner">
						<p>A dashboard app with user authentication, built in Svelte and Flask, with help from <a href="https://getbootstrap.com/">Bootstrap</a>!</p>
					</div>
				</footer>
			
			<fieldset class="form-group">
				<legend class="border-bottom mb-4">Log In</legend>
				<div class="form-group">
					<label class="form-control-label" for="email">Email: </label>
					<input id = "email" bind:value={email} />
		
				</div>
				<div class="form-group">
					<label class="form-control-label" for="email">Password: </label>
					<input type = "password" id = "password" bind:value={password} />
				</div>
			
		
			</fieldset>
			<div class="form-group">
				<button class="btn btn-outline-info" on:click={login}>
					Submit
				</button>
		</div>
		</div>
		</div>

	{/if}
</div>
</main>




