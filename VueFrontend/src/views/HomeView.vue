
<template>
    <div class="flex one">
        <h1 class="full greenColor">Welcome to <span class="redColor">Gamia</span></h1>
        <div class="flex twelve">
            <!-- left block -->
            <div class="flex one half center mygap">
                <span class="full redColor">Games</span>
                <ul v-for="game in allGames" :key="game.id">
                    <li>
                        <button class="fifth redColor menuButton">{{ game.name }}</button>
                    </li>
                </ul>

                <div>
                    <span class="redColor"> Connect</span>
                     <form @submit.prevent="handleJoin">
                        <span><input type="text"><button @click="" class="redColor menuButton">Join</button></span>
                     </form>
                </div>
            </div>
            <!-- right block  -->
            <div class="half">
                <img width=700 height=450>
            </div>
        </div>
    </div>
          <!-- <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav> -->


  <!-- <RouterView /> -->

</template>


<style scoped>


.greenColor
{
    color:#52D6B5
}

.redColor
{
    color:#F97D7B
}

.menuButton
{

    background-color: rgba(251, 190, 91, 0.14);
    padding: 2% 0 2% 0
}

.menuButton:hover
{
    transition: 0s;
    outline: solid;
    outline-color:#52D6B5;
    
}

.center
{
    text-align: center;
}

h1 
{
    font-family: "Jua", cursive;
    font-size: 64px;

}


</style>

<script>

    export default {

        mounted() {

            const getAllGames = () => {
                this.$api.get("all_games")
                .then(response => {
                    this.allGames = response.data;
                    console.log("got it")
                })
                .catch(error => {
                    setTimeout(getAllGames, 2000);
                    console.log(error)
                })
            }

            getAllGames();
        },

        data() {
            return {
                allGames: ""
            }   
        },

        methods: {
            handleJoin()
            {

            }
        }

    }
</script>