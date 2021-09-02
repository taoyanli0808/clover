export const state = () => ({
  team: '',
  project: '',
  caseName: ''
})

export const mutations = {
  setTeam (state, value) {
    state.team = value
  },
  getTeam (state) {
    return state.team
  },
  setProject (state, value) {
    state.project = value
  },
  getProject (state) {
    return state.project
  },
  setCaseName (state, value) {
    state.caseName = value
  },
  getCaseName () {
    return state.caseName
  }
}
