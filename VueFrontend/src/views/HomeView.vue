
<template>
    <div class="flex one">
        <h1 class="full" style="color:#52D6B5">Welcome to <span style="color:#F97D7B">Gamia</span></h1>
        <div class="flex two">
            <!-- left block -->
            <div class="flex half center">
                <span class="full">Games</span>
                <ul v-for="game in allGames" :key="game.id">
                    <li>
                        <button class="menuButton">{{ game.name }}</button>
                    </li>
                </ul>

                <div>
                    <span> Connect</span>
                     <form @submit.prevent="handleJoin">
                        <span><input type="text"><button @click="">Join</button></span>
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

.menuButton
{
    color: #F97D7B;
    background-color: rgba(251, 190, 91, 0.14);
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