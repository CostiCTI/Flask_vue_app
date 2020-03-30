<template>
  <div class="hello">
    <br> <br> <br> <br>
    <h1 id="m1"> {{ msg }} </h1>
    <br> <br> <br>
    <h2 id="m2"> {{ msg1 }} </h2>
    <br> <br> <br>
    <p id="par"> Challenge Platform is a place where you can have fun by solving various challenges that implies knowledge in areas
    like mathematics, computer science, crypto and others. By solving these challenges you get xp and can compare yourself 
    with the onthers. It is very important to solve the tasks by yourself but the most important thing is to learn so you shoul search
    for help only when you are blocked and you have no ideea how to solve them. Have fun! </p>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Challenge Platform',
      msg1: 'Welcome'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#m1 {
  text-align: center;
  color: green;
}
#m2 {
  text-align: center
}
#par {
  padding-left: 8%;
  padding-right: 8%;
  color: grey;
}
</style>